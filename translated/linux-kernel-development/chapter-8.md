# Chapter 8: Bottom Halves and Deferring Work

## Bottom Halves

The job of bottom halves is to perform any interrupt-related work not performed by the interrupt handler.

Since interrupt handlers run asynchronously, with at least the current interrupt line disabled, minimizing their duration is important. The following useful tips help decide how to divide the work between the top and bottom half:

- If the work is time sensitive, perform it in the interrupt handler.
- If the work is related to the hardware, perform it in the interrupt handler.
- If the work needs to ensure that another interrupt (particularly the same interrupt) does not interrupt it, perform it in the interrupt handler.
- For everything else, consider performing the work in the bottom half.

### Why Bottom Halves?

Minimizing the time spent with interrupts disabled is important for system response and performance.

Later is often simply not now. The point of a bottom half is not to do work at some specific point in the future, but simply to defer work until any point in the future when the system is less busy and interrupts are again enabled.

### A World of Bottom Halves

In the current three methods that exist for deferring work, tasklets are built on softirqs and work queues are their own subsystem.

## Softirqs

Softirqs are rarely used directly; tasklets, which are built on softirqs are a much more common form of bottom half. The softirq code lives in the file `kernel/softirq.c` in the kernel source tree.

### Implementing Softirqs

Softirqs are statically allocated at compile time. Unlike tasklets, you cannot dynamically register and destroy softirqs. Softirqs are represented by the `softirq_action` structure, which is defined in `<linux/interrupt.h>`:

```c
struct softirq_action
{
	void	(*action)(struct softirq_action *);
};
```

A 32-entry array of this structure is declared in `kernel/softirq.c`:

```c
static struct softirq_action softirq_vec[NR_SOFTIRQS];
```

Each registered softirq consumes one entry in the array. Consequently, there are `NR_SOFTIRQS` registered softirqs. The number of registered softirqs is statically determined at compile time and cannot be changed dynamically. The kernel enforces a limit of 32 registered softirqs.

#### The Softirq Handler

The prototype of a softirq handler, `action`, looks like:

```c
void softirq_handler(struct softirq_action *);
```

When the kernel runs a softirq handler, it executes this `action` function with a pointer to the corresponding `softirq_action` structure as its argument.

A softirq never preempts another softirq.

#### Executing Softirqs

A registered softirq must be marked before it will execute. This is called raising the softirq. Usually, an interrupt handler marks its softirq for execution before returning. Pending softirqs are checked for and executed in the following places:

- In the return from hardware interrupt code path
- In the ksoftirqd kernel thread
- In any code that explicitly checks for and executes pending softirqs, such as the networking subsystem

Softirq execution occurs in `__do_softirq()`, which is invoked by `do_softirq()`. If there are pending softirqs, `__do_softirq()` loops over each one, invoking its handler.

The following code is a simplified variant of the important part of `__do_softirq()`:

```c
u32 pending;

pending = local_softirq_pending();
if (pending) {
    struct softirq_action *h;

    /* reset the pending bitmask */
    set_softirq_pending(0);

    h = softirq_vec;
    do {
        if (pending & 1)
            h->action(h);
        h++;
        pending >>= 1;
    } while (pending);
}
```

It checks for, and executes, any pending softirqs. It specifically does the following:

1. It sets the pending local variable to the value returned by the `local_softirq_pending()` macro.
2. After the pending bitmask of softirqs is saved, it clears the actual bitmask.
3. The pointer `h` is set to the first entry in the `softirq_vec`.
4. If the first bit in pending is set, `h->action(h)` is called.
5. The pointer `h` is incremented by one so that it now points to the second entry in the `softirq_vec` array.
6. The bitmask `pending` is right-shifted by one.
7. The pointer `h` now points to the second entry in the array, and the pending bitmask now has the second bit as the first. Repeat the previous steps.
8. Continue repeating until pending is zero, at which point there are no more pending softirqs and the work is done.

### Using Softirqs

Softirqs are reserved for the most timing-critical and important bottom-half processing on the system.

Currently, only two subsystems directly use softirqs: networking and block devices.

Additionally, kernel timers and tasklets are built on top of softirqs.

#### Assigning and Index

Softirqs are declared statically at compile time via an `enum` in `<linux/interrupt.h>`. The kernel uses this index, which starts at zero, as a relative priority. Softirqs with the lowest numerical priority execute before those with a higher numerical priority.

Creating a new softirq includes adding a new entry to this enum. When adding a new softirq, you need to insert the new entry depending on the priority you want to give it. A new entry likely belongs in between BLOCK_SOFTIRQ and TASKLET_SOFTIRQ.

The following table contains a list of the existing tasklet types.

Tasklet | Priority | Softirq Description
------- | -------- | -------------------
HI_SOFTIRQ | 0 | High-priority tasklets
TIMER_SOFTIRQ | 1 | Timers
NET_TX_SOFTIRQ | 2 | Send network packets
NET_RX_SOFTIRQ | 3 | Receive network packets
BLOCK_SOFTIRQ | 4 | Block devices
TASKLET_SOFTIRQ | 5 | Normal priority tasklets
SCHED_SOFTIRQ | 6 | Scheduler
HRTIMER_SOFTIRQ | 7 | High-resolution timers
RCU_SOFTIRQ | 8 | RCU locking

#### Registering Your Handler

Next, the softirq handler is registered at run-time via `open_softirq()`, which takes two parameters: the softirq's index and its handler function.

The softirq handlers run with interrupts enabled and cannot sleep.While a handler runs, softirqs on the current processor are disabled.Another processor, however, can execute other softirqs. If the same softirq is raised again while it is executing, another processor can run it simultaneously. This means that any shared data—even global data used only within the softirq handler—needs proper locking. Consequently, most softirq handlers resort to per-processor data and other tricks to avoid explicit locking and provide excellent scalability.

The reason for using softirqs is scalability.

#### Raising Your Softirq

To mark it pending, so it is run at the next invocation of `do_softirq()`, call `raise_softirq()`.

This function disables interrupts prior to actually raising the softirq and then restores them to their previous state. If interrupts are already off, the function `raise_softirq_irqoff()` can be used as a small optimization.

Softirqs are most often raised from within interrupt handlers.

## Tasklets

Tasklets are a bottom-half mechanism built on top of softirqs.

### Implementing Tasklets

Tasklets are represented by two softirqs: `HI_SOFTIRQ` and `TASKLET_SOFTIRQ`. The only difference in these types is that the `HI_SOFTIRQ`-based tasklets run prior to the `TASKLET_SOFTIRQ`-based tasklets.

#### The Tasklet Structure

Tasklets are represented by the `tasklet_struct` structure. Each structure represents a unique tasklet. The structure is declared in `<linux/interrupt.h>`:

```c
struct tasklet_struct {
    struct tasklet_struct *next;  /* next tasklet in the list */
    unsigned long state;          /* state of the tasklet */
    atomic_t count;               /* reference counter */
    void (*func)(unsigned long);  /* tasklet handler function */
    unsigned long data;           /* argument to the tasklet function */
};
```

The `func` member is the tasklet handler and receives data as its sole argument.

The state member is exactly zero, `TASKLET_STATE_SCHED`, or `TASKLET_STATE_RUN`. `TASKLET_STATE_SCHED` denotes a tasklet that is scheduled to run, and `TASKLET_STATE_RUN` denotes a tasklet that is running.As an optimization, `TASKLET_STATE_RUN` is used only on multiprocessor machines because a uniprocessor machine always knows whether the tasklet is running.

The `count` field is used as a reference count for the tasklet. If it is nonzero, the tasklet is disabled and cannot run; if it is zero, the tasklet is enabled and can run if marked pending.

#### Scheduling Tasklets

`Scheduled` tasklets are stored in two per-processor structures: `tasklet_vec` (for regular tasklets) and `tasklet_hi_vec` (for high-priority tasklets). Both of these structures are linked lists of `tasklet_struct` structures. Each `tasklet_struct` structure in the list represents a different tasklet.

Tasklets are scheduled via the `tasklet_schedule()` and `tasklet_hi_schedule()` functions, which receive a pointer to the tasklet’s `tasklet_struct` as their lone argument. Each function ensures that the provided tasklet is not yet scheduled and then calls `__tasklet_schedule()` and `__tasklet_hi_schedule()` as appropriate. The two functions are similar. Now, let’s look at the steps `tasklet_schedule()` undertakes:

1. Check whether the tasklet’s state is `TASKLET _ STATE_SCHED`. If it is, the tasklet is already scheduled to run and the function can immediately return.
2. Call `__tasklet_schedule()`.
3. Save the state of the interrupt system, and then disable local interrupts.This ensures that nothing on this processor will mess with the tasklet code while `tasklet_schedule()` is manipulating the tasklets.
4. Add the tasklet to be scheduled to the head of the `tasklet_vec` or `tasklet_hi_vec` linked list, which is unique to each processor in the system.
5. Raise the `TASKLET_SOFTIRQ` or `HI_SOFTIRQ` softirq, so `do_softirq()` executes this tasklet in the near future.
6. Restore interrupts to their previous state and return.

At the `do_softirq()` is run as discussed in the previous section. Because most tasklets and softirqs are marked pending in interrupt handlers, `do_softirq()` most likely runs when the last interrupt returns. Because `TASKLET_SOFTIRQ` or `HI_SOFTIRQ` is now raised, `do_softirq()` executes the associated handlers. These handlers, `tasklet_action()` and `tasklet_hi_action()`, are the heart of tasklet processing. Let’s look at the steps these handlers perform:

1. Disable local interrupt delivery and retrieve the `tasklet_vec` or `tasklet_hi_vec` list for this processor.
2. Clear the list for this processor by setting it equal to `NULL`.
3. Enable local interrupt delivery. There is no need to restore them to their previous state because this function knows that they were always originally enabled.
4. Loop over each pending tasklet in the retrieved list.
5. If this is a multiprocessing machine, check whether the tasklet is running on another processor by checking the `TASKLET_STATE_RUN` flag. If it is currently running, do not execute it now and skip to the next pending tasklet.
6. If the tasklet is not currently running, set the `TASKLET_STATE_RUN` flag, so another processor will not run it.
7. Check for a zero count value, to ensure that the tasklet is not disabled. If the tasklet is disabled, skip it and go to the next pending tasklet.
8. Run the tasklet handler.
9. After the tasklet runs, clear the `TASKLET_STATE_RUN` flag in the tasklet’s state field.
10. Repeat for the next pending tasklet, until there are no more scheduled tasklets waiting to run.

### Using Tasklets

#### Declaring Your Tasklet

You can create tasklets statically or dynamically, depending on whether you have (or want) a direct or indirect reference to the tasklet. If you are going to statically create the tasklet (and thus have a direct reference to it), use one of two macros in `<linux/interrupt.h>`:

```c
DECLARE_TASKLET(name, func, data)
DECLARE_TASKLET_DISABLED(name, func, data);
```

Both these macros statically create a struct `tasklet_struct` with the given name. When the tasklet is scheduled, the given function `func` is executed and passed the argument `data`. The difference between the two macros is the initial reference count. The first macro creates the tasklet with a count of zero, and the tasklet is enabled. The second macro sets count to one, and the tasklet is disabled.

To initialize a tasklet given an indirect reference (a pointer) to a dynamically created `struct tasklet_struct` named `t`, call `tasklet_init()`:

```c
tasklet_init(t, tasklet_handler, dev); /* dynamically as opposed to statically */
```

#### Writing Your Tasklet Handler

The tasklet handler must match the correct prototype:

```c
void tasklet_handler(unsigned long data)
```

As with softirqs, tasklets cannot sleep. This means you cannot use semaphores or other blocking functions in a tasklet. Tasklets also run with all interrupts enabled, so you must take precautions if your tasklet shares data with an interrupt handler. Unlike softirqs, however, two of the same tasklets never run concurrently. If your tasklet shares data with another tasklet or softirq, you need to use proper locking.

#### Scheduling Your Tasklet

To schedule a tasklet for execution, `tasklet_schedule()` is called and passed a pointer to the relevant `tasklet_struct`:

```c
tasklet_schedule(&my_tasklet); /* mark my_tasklet as pending */
```

If the same tasklet is scheduled again, before it has had a chance to run, it still runs only once. If it is already running, the tasklet is rescheduled and runs again.

You can disable a tasklet via a call to `tasklet_disable()`, which disables the given tasklet. If the tasklet is currently running, the function will not return until it finishes executing. Alternatively, you can use `tasklet_disable_nosync()`, which disables the given tasklet but does not wait for the tasklet to complete prior to returning. A call to `tasklet_enable()` enables the tasklet. This function also must be called before a tasklet created with `DECLARE_TASKLET_DISABLED()` is usable.

You can remove a tasklet from the pending queue via `tasklet_kill()`. This function receives a pointer as a lone argument to the tasklet's `tasklet_struct`. This function first waits for the tasklet to finish executing and then it removes the tasklet from the queue. Nothing stops some other code from rescheduling the tasklet. This function must not be used from interrupt context because it sleeps.

#### ksoftirqd

Softirq processing is aided by a set of per-processor kernel threads. These kernel threads help in the processing of softirqs when the system is overwhelmed with softirqs.

The solution ultimately implemented in the kernel is to not immediately process reactivated softirqs. Instead, if the number of softirqs grows excessive, the kernel wakes up a family of kernel threads to handle the load. The kernel threads run with the lowest possible priority (nice value of 19), which ensures they do not run in lieu of anything important.

There is one thread per processor, each named `ksoftirqd/n` where `n` is the processor number. On a two-processor system, they are `ksoftirqd/0` and `ksoftirqd/1`. Having a thread on each processor ensures an idle processor, if available, can always service softirqs. After the threads are initialized, they run a tight loop similar to this:

```c
for (;;) {
    if (!softirq_pending(cpu))
        schedule();

    set_current_state(TASK_RUNNING);

    while (softirq_pending(cpu)) {
        do_softirq();
        if (need_resched())
            schedule();
    }

    set_current_state(TASK_INTERRUPTIBLE);
}
```

## Work Queues

Work queues defer work into a kernel thread which always runs in process context. Thus, code deferred to a work queue has all the usual benefits of process context. Most important, work queues are schedulable and can therefore sleep.

If you need a schedulable entity to perform your bottom-half processing, you need work queues. They are the only bottom-half mechanisms that run in process context, and thus the only ones that can sleep.

### Implementing Work Queues

In its most basic form, the work queue subsystem is an interface for creating kernel threads to handle work queued from elsewhere. The kernel threads are called `worker threads`. Work queues let your driver create a special worker thread to handle deferred work. The work queue subsystem, however, implements and provides a default worker thread for handling work. Therefore, in its most common form, a work queue is a simple interface for deferring work to a generic kernel thread.

The default worker threads are called `events/n` where `n` is the processor number.

#### Data Structure Representing the Threads

The worker threads are represented by the workqueue_struct structure:

```c
/*
 * The externally visible workqueue abstraction is an array of
 * per-CPU workqueues:
 */
struct workqueue_struct {
    struct cpu_workqueue_struct cpu_wq[NR_CPUS];
    struct list_head list;
    const char *name;
    int singlethread;
    int freezeable;
    int rt;
};
```

This structure, defined in `kernel/workqueue.c`, contains an array of `struct cpu_workqueue_struct`, one per processor on the system. Because the worker threads exist on each processor in the system, there is one of these structures per worker thread, per processor, on a given machine. The `cpu_workqueue_struct` is the core data structure and is also defined in `kernel/workqueue.c`:

```c
struct cpu_workqueue_struct {
    spinlock_t lock;             /* lock protecting this structure */
    struct list_head worklist;   /* list of work */
    wait_queue_head_t more_work;
    struct work_struct *current_struct;
    struct workqueue_struct *wq; /* associated workqueue_struct */
    task_t *thread;              /* associated thread */
};
```

Note that each type of worker thread has one `workqueue_struct` associated to it. Inside, there is one `cpu_workqueue_struct` for every thread and, thus, every processor, because there is one worker thread on each processor.

#### Data Structure Representing the Work

All worker threads are implemented as normal kernel threads running the `worker_thread()` function. After initial setup, this function enters an infinite loop and goes to sleep. When work is queued, the thread is awakened and processes the work. When there is no work left to process, it goes back to sleep.

The work is represented by the work_struct structure, defined in `<linux/workqueue.h>`:

```c
struct work_struct {
    atomic_long_t data;
    struct list_head entry;
    work_func_t func;
};
```

These structures are strung into a linked list, one for each type of queue on each processor.

When a worker thread wakes up, it runs any work in its list. As it completes work, it removes the corresponding work_struct entries from the linked list. When the list is empty, it goes back to sleep.

The core of `worker_thread` is simplified as follows:

```c
for (;;) {
    prepare_to_wait(&cwq->more_work, &wait, TASK_INTERRUPTIBLE);
    if (list_empty(&cwq->worklist))
        schedule();
    finish_wait(&cwq->more_work, &wait);
    run_workqueue(cwq);
}
```

This function performs the following functions, in an infinite loop:

1. The thread marks itself sleeping (the task's state is set to `TASK_INTERRUPTIBLE`) and adds itself to a wait queue.
2. If the linked list of work is empty, the thread calls `schedule()` and goes to sleep.
3. If the list is not empty, the thread does not go to sleep. Instead, it marks itself `TASK_RUNNING` and removes itself from the wait queue.
4. If the list is nonempty, the thread calls `run_workqueue()` to perform the deferred work.

The function `run_workqueue()` actually performs the deferred work:

```c
while (!list_empty(&cwq->worklist)) {
    struct work_struct *work;
    work_func_t f;
    void *data;
    work = list_entry(cwq->worklist.next, struct work_struct, entry);
    f = work->func;
 list_del_init(cwq->worklist.next);
    work_clear_pending(work);
    f(work);
}
```

This function loops over each entry in the linked list of pending work and executes the `func` member of the `workqueue_struct` for each entry in the linked list:

1. While the list is not empty, it grabs the next entry in the list.
2. It retrieves the function that should be called, `func`, and its argument, `data`.
3. It removes this entry from the list and clears the pending bit in the structure itself.
4. It invokes the function.
5. Repeat.

#### Work Queue Implementation Summary

![img](./pic/ch8_1.png)

At the highest level, there are worker threads. There can be multiple types of worker threads; there is one worker thread per processor of a given type. Parts of the kernel can create worker threads as needed. By default, there is the `events` worker thread. Each worker thread is represented by the `cpu_workqueue_struct` structure. The `workqueue_struct` structure represents all the worker threads of a given type.

The driver creates work, which it wants to defer to later. The `work_struct` structure represents this work. This structure contains a pointer to the function that handles the deferred work. The work is submitted to a specific worker thread. The worker thread then wakes up and performs the queued work.

### Using Work Queues

#### Creating Work

The first step is actually creating some work to defer. To create the structure statically at runtime, use `DECLARE_WORK`:

```c
DECLARE_WORK(name, void (*func)(void *), void *data);
```

This statically creates a `work_struct` structure named `name` with handler function `func` and argument `data`.

Alternatively, you can create work at runtime via a pointer:

```c
INIT_WORK(struct work_struct *work, void (*func)(void *), void *data);
```

This dynamically initializes the work queue pointed to by `work` with handler function `func` and argument `data`.

#### Your Work Queue Handler

The prototype for the work queue handler is:

```c
void work_handler(void *data)
```

A worker thread executes this function, so the function runs in process context. By default, interrupts are enabled and no locks are held. If needed, the function can sleep.

#### Scheduling Work

Now that the work is created, we can schedule it. To queue a given work's handler function with the default events worker threads, call:

```c
schedule_work(&work);
```

The work is scheduled immediately and is run as soon as the `events` worker thread on the current processor wakes up.

Sometimes you do not want the work to execute immediately, but instead after some delay. You can schedule work to execute at a given time in the future:

```c
schedule_delayed_work(&work, delay);
```

In this case, the `work_struct` represented by `&work` will not execute for at least `delay` timer ticks into the future.

#### Flushing Work

Sometimes, you need to ensure that a given batch of work has completed before continuing. Modules almost certainly want to call this function before unloading, and other places in the kernel also might need to ensure that no work is pending, to prevent race conditions.

For these needs, there is a function to flush a given work queue:

```c
void flush_scheduled_work(void);
```

This function waits until all entries in the queue are executed before returning. While waiting for any pending work to execute, the function sleeps. Therefore, you can call it only from process context.

Note that this function does not cancel any delayed work.

#### Creating New Work Queue

You create a new work queue and the associated worker threads via a simple function:

```c
struct workqueue_struct *create_workqueue(const char *name);
```

The parameter `name` is used to name the kernel threads.

Creating work is handled in the same manner regardless of the queue type. After the work is created, the following functions are analogous to `schedule_work()` and `schedule_delayed_work()`, except that they work on the given work queue and not the default events queue.

```c
int queue_work(struct workqueue_struct *wq, struct work_struct *work)

int queue_delayed_work(struct workqueue_struct *wq,
                       struct work_struct *work,
                       unsigned long delay)
```

Finally, you can flush a wait queue via a call to the function:

```c
flush_workqueue(struct workqueue_struct *wq)
```

As previously discussed, this function works identically to `flush_scheduled_work()`, except that it waits for the given queue to empty before returning.

## Which Bottom Half Should I Use?

`Softirqs`, by design, provide the least serialization. This requires softirq handlers to go through extra steps to ensure that shared data is safe because two or more softirqs of the same type may run concurrently on different processors. If the code in question is already highly threaded, such as in a networking subsystem that is chest-deep in per-processor variables, softirqs make a good choice. They are certainly the fastest alternative for timing-critical and high-frequency uses.

`Tasklets` make more sense if the code is not finely threaded. They have a simpler interface and, because two tasklets of the same type might not run concurrently, they are easier to implement. Tasklets are effectively softirqs that do not run concurrently. A driver developer should always choose tasklets over softirqs, unless prepared to utilize per-processor variables or similar magic to ensure that the softirq can safely run concurrently on multiple processors.

If the deferred work needs to run in process context, the only choice of the three is `work queues`. If process context is not a requirements (specifically, if you have no need to sleep), softirqs or tasklets are perhaps better suited. Work queues involve the highest overhead because they involve kernel threads and, therefore, context switching. This doesn't mean they are inefficient, but in light of thousands of interrupts hitting per second (as the networking subsystem might experience), other methods make more sense. However, work queues are sufficient for most situations.

The following table is a comparison between the three bottom-half interfaces:

Bottom Half | Context | Inherent Serialization
----------- | ------- | ----------------------
Softirq | Interrupt | None
Tasklet | Interrupt | Against the same tasklet
Work queues | Process | None (scheduled as process context)

## Locking Between the Bottom Halves

It is crucial to protect shared data from concurrent access while using bottom halves, even on a single processor machine. A bottom half can run at virtually any moment.

One benefit of tasklets is that they are serialized with respect to themselves. The same tasklet will not run concurrently, even on two different processors. This means you do not have to worry about intra-tasklet concurrency issues. Inter-tasklet concurrency (when two different tasklets share the same data) requires proper locking.

Because softirqs provide no serialization, (even two instances of the same softirq might run simultaneously), all shared data needs an appropriate lock.

If process context code and a bottom half share data, you need to disable bottom-half processing and obtain a lock before accessing the data. Doing both ensures local and SMP protection and prevents a deadlock.

If interrupt context code and a bottom half share data, you need to disable interrupts and obtain a lock before accessing the data.This also ensures both local and SMP protection and prevents a deadlock.

Any shared data in a work queue requires locking, too.The locking issues are no different from normal kernel code because work queues run in process context.

## Disabling Bottom Halves

To safely protect shared data, you usually need to obtain a lock and disable bottom halves.

The following table is a summary of these functions:

Method | Description
------ | -----------
void local_bh_disable() | Disables softirq and tasklet processing on the local processor
void local_bh_enable() | Enables softirq and tasklet processing on the local processor

The calls can be nested; only the final call to `local_bh_enable()` actually enables bottom halves.

The functions accomplish this by maintaining a per-task counter via the `preempt_count`, the same counter used by kernel preemption. When the counter reaches zero, bottom-half processing is possible. Because bottom havels were disabled, `local_bh_enable()` also checks for any pending bottom halves and executes them.

The functions are unique to each supported architecture and are usually written as complicated macros in `<asm/softirq.h>`. The following are close C representations:

```c
/*
* disable local bottom halves by incrementing the preempt_count
*/
void local_bh_disable(void)
{
    struct thread_info *t = current_thread_info();
    t->preempt_count += SOFTIRQ_OFFSET;
}

/*
* decrement the preempt_count - this will ‘automatically’ enable
* bottom halves if the count returns to zero
*
* optionally run any bottom halves that are pending
*/
void local_bh_enable(void)
{
    struct thread_info *t = current_thread_info();
    t->preempt_count -= SOFTIRQ_OFFSET;

    /*
    * is preempt_count zero and are any bottom halves pending?
    * if so, run them
    */
    if (unlikely(!t->preempt_count && softirq_pending(smp_processor_id())))
        do_softirq();
}
```

These calls do not disable the execution of work queues. Because work queues run in process context, there are no issues with asynchronous execution. Because softirqs and tasklets can occur asynchronously, kernel code may need to disable them.With work queues, on the other hand, protecting shared data is the same as in any process context.
