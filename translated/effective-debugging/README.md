# Effective Debugging

- [Macro Strategy](#Macro Strategy)
- [Usual Methods and Practices](#Usual Methods and Practices)
- [General Tools and Techniques](#General Tools and technology)
- [Debugger usage skills](#Debugger usage skills)
- [Programming technology](#Programming technology)
- [Compile-time debugging technology](#Compilation-time debugging technology )
- [Runtime debugging technology](#Runtime debugging technology)

## Macro strategy

1. Handle all problems
 through the transaction tracking system
 - GitHub/GitLab
 - Ensure that every transaction is Ability to accurately describe a new approach to a problem using short, self-contained, and correct examples. 
 - Categorizes issues and schedules work based on the priority and severity of each issue. 
2. Search the Internet for the exact problem you encountered to seek inspiration for solving the problem
 - Put double quotes around the error message to search accurately on the Internet. 
 - Carefully check the answers on the StackExchange series of websites. 
3. Ensure that both pre-conditions and post-conditions are met
4. Start with the specific problem and trace the bug upward, or start with the high-level program and trace the bug downward
 - If the cause of the fault can be clearly pointed out, then you should start from the bottom. Look up for errors, such as when a program crashes, when a program freezes, when a program issues an error message, etc. 
 - If the cause of the failure is difficult to pinpoint, you should look for the error from the top down, for example, when you encounter performance issues, security issues, and reliability issues. 
5. Look for differences between a functioning system and a failing system
 - Consider all factors that affect system behavior, including code, input, call parameters, environment variables, services, and dynamic link libraries . 
 - strace, ltrace, truss, tcpdump, wireshark, ldd, nm
 - Binary search
 - diff, cut, awk, grep, comm
6. Use the software's own debugging mechanism
 - Find out what you are debugging The debugging mechanism supported by the software and use it to troubleshoot problems. 
7. Try to use multiple tools to build software and run it in different environments
8. Focus on the most important issues

## Common methods and practices

9. Believe that you can debug the problem well
10. Efficiently reproduce the problem in the program
 - If you can accurately reproduce the problem in the reproduction, then our debugging process will be simplified. 
 - Create a short, self-contained example that reproduces a problem in your program. 
 - Try to create an execution environment that can be copied
 - Use a version control system to mark a specific software version so that the corresponding code can be obtained based on this mark
11. After modifying the code, you must be able to modify it as soon as possible See results
 - Try to see the results as soon as possible after modifying the code to improve debugging efficiency. 
 - Configure a rapid automated build and deployment process. 
 - When testing software, make sure it exposes faults as quickly as possible. 
12. Automate complex test scenarios
 - Automatically execute complex test cases through scripting languages. 
13. Allow yourself to observe as much debugging-related data as possible
14. Consider updating the software
 - Retry the code you wrote in the updated environment. 
 - Consider the possibility of bugs caused by third-party components. 
15. View the source code of third-party components to understand their usage
 - If you rely on a third-party component, you should obtain its source code. 
 - Explore issues related to third-party APIs and some strange error messages by looking at the source code of third-party components. 
 - To link against debug versions of third-party libraries. 
16. Use specialized monitoring and testing equipment
 - a logic analyzer, bus analyzer or protocol analyzer can help you pinpoint problems closer to the hardware level. 
 - Monitor network packets by combining Wireshark with an Ethernet hub, using a managed switch, or command line capture. 
17. Make faults more prominent
 - Force the software to execute suspicious paths. 
 - Increases the amplitude of certain effects to make them more prominent. 
 - Stresses the software, forcing it out of a comfortable state where it can handle load gracefully. 
 - Temporarily create a branch in the version management system and put all changes on this branch. 
18. Debug unusable systems from your own desktop computer 
 - Configure the device emulator to debug mobile apps from your computer screen and keyboard. 
 - Set up a shim mechanism to debug embedded code using tools from your own computer. 
 - Prepares for remote access so that the customer's computer can be debugged remotely. 
 - Configure a KVM over IP device to debug problems on remote servers. 
19. Automate debugging tasks
20. Clean up the program before and after debugging
 - Before you start debugging major bugs, make sure the code is clean. 
 - After debugging, the temporary changes made to the code during the debugging process must be restored, and the useful code must be submitted to the code base. 
21. Fix all problems of the same type

## Common tools and techniques

22. Use Unix command line tools to analyze debugging data
 - use the pipe symbol "`|`"
 - awk, sed, grep, fgrep, find, sort, uniq, diff, comm, wc, head, tail, xargs
 - Redirect 
23. Master the various options and idioms of command line tools
24. Use the editor to browse the data required when debugging the program
25. Optimize the working environment
 - PATH environment variables, shell and editor, command aliases, tool related Environment variables, history
 - export, set, alias, shopt
26. Use the version control system to find the cause and process of the bug
 - git log, git blame, git rev-list, git show, git diff, git checkout, git bisect, git reset, git merge, git stash save, git stash pop
27. Use tools to monitor a system composed of multiple independent programs

## Tips on using debuggers 

28. Include symbol information when compiling code to facilitate debugging
 - Adjust the configuration options used to build the program so that the level of debugging information matches your needs. 
 - Disables the compiler's code optimization features so that the generated code corresponds to the code you want to debug. 
29. Single-step debugging of the code
 - Use single-step debugging to view the execution sequence of statements and the status of the program. 
 - In order to speed up debugging, we can go directly through certain parts that are not related to the bug without entering them. 
 - If you find a problem with a routine that the program passes through, set a breakpoint for the routine, re-run the program, and enter the routine for single-step debugging to narrow the scope of troubleshooting. 
30. Set code breakpoints and data breakpoints
 - Use code breakpoints to reduce the scope of code that needs attention. 
 - If a certain piece of code will be executed many times, and only a few of them are of concern to you, then set a breakpoint upstream of its execution path first, and then set a breakpoint for this piece of code after the program is paused. . 
 - If you want to debug an abnormal exit, set a terminal breakpoint on the exception or on the routine that the program calls when it exits. 
 - If the program becomes unresponsive, it can be stopped in the debugger. 
 - Use data breakpoints to target bugs that cause variable values ​​to change unexpectedly. 
31. Understand the reverse debugging function
32. View the mutual calls between routines
 - View the stack information of the program to understand its execution status. 
 - If the stack information is messy, it means there may be something wrong with the code. 
33. Check the values ​​of variables and expressions to find errors in the program
 - Validate important expressions to see if their values ​​are correct. 
 - Sets the debugger to continuously display changes in expressions as the algorithm executes. 
 - Use local variables to understand the running logic of the routine. 
 - Use data visualization mechanisms to display complex data structures. 
34. Learn how to attach a debugger to a running process
35. Learn how to use core dump information for debugging
36. Set up debugging tools
 - Use a debugger with a graphical interface. 
 - Configure gdb so that it can save entered commands and set a set of shortcut keys for symbols that you are accustomed to using. 
 - Put commonly used commands in gdb scripts. 
 - After modifying the source code, you can build the program directly in gdb without restarting gdb, so as to retain the commands you entered during this debugging session. 
37. Learn to view assembly code and original memory
 - View the disassembled machine instructions to understand the underlying operation of the program code. 
 - Look in the eax or r0 register for the function's return value. 
 - View the in-memory representation of the data to understand how it is stored under the hood. 

## Programming Technology

38. Review suspicious codes and manually exercise these codes
 - Check whether there are common errors in the code. 
 - Manually execute the code to verify that it is correct. 
 - Parse complex data structures through plotting. 
39. Review the code and discuss it with colleagues
 - Explain the code to the little yellow duck. 
40. Add debugging mechanism to the software
 - Add an option to the program to enable it to enter debugging mode. 
 - Add corresponding debugging commands to enable the debugger to manipulate the state of the program, record the operations it performs, reduce the complexity of its runtime program, quickly jump between its user interfaces, and display complex data structures . 
 - Adds command line, web, and serial connection interfaces and interfaces for debugging embedded devices and servers. 
 - Use commands in debug mode to simulate errors related to external factors. 
41. Add logging
 - Use logging statements to build a basic debugging platform that can be maintained permanently. 
42. Unit testing the software
 - Check suspicious routines with unit tests to find bugs in them. 
43. Debugging with assertions
 - Use assertion statements that complement unit tests to more accurately target errors in your code. 
 - Use assertion statements to debug complex algorithms to verify whether their pre-conditions, invariant conditions and post-conditions are true. 
44. Modify the program under test to verify your assumptions
 - Manually set certain values ​​in the code to verify which values ​​are correct and which values ​​are incorrect. 
45. Minimize the gap between correct examples and erroneous code
46. Simplify suspect code
 - Selectively remove large sections of code to make errors more prominent. 
 - Split a complex statement or function into multiple smaller parts to monitor or test its functionality individually. 
 - Consider deprecating complex algorithms that may cause bugs and implementing simpler algorithms instead. 
47. Rewrite the suspect code in another programming language
 - Use another more expressive language to rewrite difficult-to-fix code to reduce the number of statements that may cause problems. 
 - Port the buggy code to a better programming environment so that more powerful debugging tools can be used to solve the problems. 
48. Improve the readability and structure of suspect code
 - Refactor the code to eliminate complex structures that are of poor quality. 
49. Know the root cause of a bug, not just eliminate its symptoms
 - Don't use ad hoc code to get around the superficial symptoms of your program, but find the underlying cause of the bug and fix it. 
 - Use as general a method as possible to handle complex situations, rather than just fixing some of the special cases. 

## Compile-time debugging techniques

50. Inspect the generated code
 - View the automatically generated code to understand the corresponding compile-time and run-time issues in the source code. 
 - Display this automatically generated code into an easy-to-read form through compiler options or specific tools. 
51. Use static program analysis tools
 - Configure the compiler so that it can properly analyze the program and find bugs in it. 
 - Incorporate at least one static program analysis tool into your build process and continuous integration process. 
52. Configure the project so that the program can be built and executed in a fixed way
53. Configure the libraries used for debugging and the checks that are performed when building the code
 - In your development environment, find Check out the runtime debugging features supported by the compiler and libraries and enable them. 

## Runtime debugging technology

54. Find errors by building test cases
 - Build a reliable and simplest test case. In the process, you may find problems in the program and its solutions. 
 - Embed test cases into the program as unit tests or regression tests. 
55. Make the software exit as soon as possible when encountering problems
56. Review the application's log files
57. Perform performance evaluation of operations performed by the system and processes
 - Check CPU, I/O and memory usage and Saturation to analyze performance issues. 
58. Track program execution
 - Track system and library calls and monitor program behavior without accessing the source code. 
59. Use dynamic program analysis tools
