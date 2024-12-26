# Android security attack and defense practice

## Chapter 1 Android development tools

### Use the command line to create an Android virtual device (AVD)

1. Obtain a list of usable system images

 ```sh
[path-to-sdk-install]/tools/android list targets
```

2. Create AVD

```sh
[path-to-sdk-install]/tools/android create -avd -n [AVD name] -t [system image target id]

// more external storage 
[path-to-sdk-install]/tools/android create -avd -n [AVD name] -t [system image target id] -c [size] [K|M]
```

3. Run the created AVD

```sh
[path-to-sdk-install]/tools/emulator -avd [AVD name]
 
// specify internal storage
[path-to-sdk-install]/tools/emulator -avd [AVD name] -partition-size [size in MBs]
```

Extended reading: <https://developer.android.com/studio/tools/help/android.html>

### Using Android Debug Bridge (ADB) with AVD interaction

1. Start the specified AVD

```sh
[path-to-sdk-install]/tools/emulator -avd [name]
```

2. List all connected Android devices

```sh
[path-to-sdk-install[/platform-tools/adb devices
 ```

3. Run a shell

 connected to the Android device ```sh
/sdk/platform-tools/adb shell
```

Extended reading: <https://developer.android.com/studio/command-line/adb.html>

### Copy files from/to AVD 

1. Copy the file from AVD

```sh
adb {options} pull [path to copy from] [local path to copy to]
```

2. Copy the file to AVD

```sh
adb {options} push [local path to copy from] [path to copy to on AVD]
 ```

### Install app

 in AVD via ADB```sh
adb {options} install [path to apk]
```

## Chapter 2 Practice app security

### Check the app’s certificate and signature

1. Remove an app

``` from Android sh
/sdk/platform-tools/adb pull /system/app/Calendar/Calendar.apk
```

2. Unzip apk

```sh
unzip Calendar.apk
```

3. In the folder "META_INF"

- `MANIFEST.MF`: Declared resources, and `CERT .SF` files are similar. 
- `CERT.RSA`: Public key certificate. 
- `CERT.SF`: Contains all resource files in the app and is responsible for signing the app. 

```sh
[jdk]/bin/keytool -printcert -file META-INF/CERT.RSA
```

4. View the contents of the signature file, including each file in the app The cryptographic hash of the resource file. 

```sh
cat [path-to-unzipped-apk]/META-INF/CERT.SF
```

5. Use OpenSSL to view the certificate

```sh% 0Aopenssl pkcs7 -inform DER -in META-INF/CERT.RSA -noout -print_certs -text
```

Extended reading:

- <https://datatracker.ietf.org/doc/rfc2459/?include_text=1>
- <http://docs.oracle .com/javase/6/docs/technotes/guides/security/cert3.html>

### for Android app signature

 First delete the existing `META-INF` folder, and then create a signature. 

1. Create a keystore (keystore) to store the private key used to sign the app. And put this key storage in a safe place. 

```sh
// Generate 
keytool -genkey -v -keystore [nameofkeystore] -alias [your_keyalias] -keyalg RSA -keysize 2048 -validity [numberofdays]
// Delete 
keytool -delete - alias [your_keyalias] -keystore [nameofkeystore] -storepass [password]
```

```text
/usr/local/java/jdk1.8.0_112/bin/keytool -genkey -v -keystore releasekey.keystore -alias keyalias -keyalg RSA 
Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=gasp
Enter the keystore password: 
What is your first and last name?
 [Unknown]: Li Hua
What is the name of your organizational unit?
 [Unknown]: Xi dian
What is the name of your organization?
 [Unknown] : Mo Ha Xie Hui
What is the name of your city or region?
 [Unknown]: xi'an
What is the name of your province/city/autonomous region?
 [Unknown]: shanxi
What is the two-letter country code for this unit?
 [Unknown]: China
CN=Li Hua, OU=Xi dian, O=Mo Ha Xie Hui, L=xi'an, ST=shanxi, Is C=China correct?
 [No]: y

 Generating a 2,048-bit RSA key pair and self-signed certificate (SHA256withRSA) for the following objects (valid for 90 days):
 CN=Li Hua, OU=Xi dian, O=Mo Ha Xie Hui, L=xi'an, ST=shanxi, C=China
Enter the key password of <keyalias>
 (if Same as the keystore password, press Enter): 
[Storing releasekey.keystore]
```

2. Use this key store to sign an app. 

```sh
jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore [name of your keystore] [your .apk file] [your key alias]
```

`Keytool` Yes The actual way to deal with public and private keys is: put the public key in X.509 v3 In the certificate, the certificate is used to declare the public key holder and can verify whether the relevant public key belongs to the declared holder. 

Extended reading:

- <http://docs.oracle.com/javase/6/docs/technotes/tools/windows/jarsigner.html>
- <http://docs.oracle .com/javase/6/docs/technotes/tools/solaris/keytool.html>
- <https://developer.android.com/studio/publish/app-signing.html>

### Verify the app’s signature

```sh
jarsigner -verify -verbose [path-to -yout-apk]
```

### Explore the AndroidManifest.xml file

 and extract it from the apk package AndroidManifest.xml file. 

```sh
apktool d -f -s [apk file] -o decoded-data/
```

The extracted file is now in the decoded-data folder. 

Extended reading: <https://developer.android.com/guide/topics/manifest/manifest-intro.html>

### Interacting with the activity manager through ADB

1. Get A shell

```sh
adb shell
```

2. Find one to run activity

```sh
pm list packages
```

3. Run activity

```sh
am start [package name]
```

4. Running activity Previously, you could also specify the intent passed to the activity by using the `intent` parameter received by the `start` command. 

```sh
am start <INTENT> < --user UID | current >
```

We can execute the following or similar commands: 

```sh% 0Aam start -n com.android.MyPackage/
com.android.MyPackageLaunchMeActivity
-e MyInput HelloWorld -a android.intent.MyPackageIntentAction
-c android.intent.category.MyPackageIntentCategory
```

You can also use the activity manager to start the service:

``sh
am startservice <package name> /<component name> <INTENT>
```

 You can also use a command similar to the following: 

```sh
am startservice com.android.app/
com.android.app.service.ServiceComponent% 0A```

Of course, we can also use the activity manager to kill a process:

```sh
kill < --user UID | current > <package>
```

Extended reading:<https://developer.android.com/studio/command-line/adb.html>

### Extract resources in the app through ADB 

1. Get a shell and switch to the `/data/data/` directory

```sh
adb shell
cd /data/data/
```

Note the owner and group of the `data` directory. The owner is actually the app itself. 

2. View the app’s resources and metadata

```sh
ls -alR */
ls -alR */files/
ls -al */*/*.mp3
``` 

3. After finding the file, you can copy the file

```sh
adb pull /data/data/[package-name]/[filepath]
```

## Chapter 3 Android Security Assessment Tool

### Introduction

Santoku: Debian-based Linux distribution version for mobile security assessment. 

Drozer: An exploit and Android security assessment framework. Drozer is divided into two parts, one is the console, which runs on the local computer, and the other is the server, which is an app installed on the target Android device. When you use the console to interact with an Android device, you enter Java code into the drozer agent running on the actual device. 

### Run a drozer session

1. Using ADB, set up port forwarding

```sh
adb forward tcp:31415 tcp:31415
```

2. Open drozer's agent on the device and enable the agent. 

3. Connect drozer console and enter console mode

```sh
drozer console connect
```

### Enumerate installed packages

```sh 
dz> run app.package.list

dz> run app.package.list -f [application name]

dz> run app.package.info --package [package name]
OR
dz> run app.package.info -a [package name]

dz> run app.package.info -p [permission label]
```

 works: <https://github.com/mwrlabs/drozer/blob/develop/src/drozer/modules/app/package.py>

```py
 def add_arguments(self, parser):
 parser.add_argument("-a", "--package", default=None, help="the identifier of the package to inspect")
 parser.add_argument("-d" , "--defines-permission", default=None, help="filter by the permissions a package defines")
 parser.add_argument("-f", "--filter", default=None, help="keyword filter conditions")
        parser.add_argument("-g", "--gid", default=None, help="filter packages by GID")
        parser.add_argument("-p", "--permission", default=None, help="permission filter conditions")
        parser.add_argument("-u", "--uid", default=None, help="filter packages by UID")
        parser.add_argument("-i", "--show-intent-filters", action="store_true", default=False , help="show intent filters")

    def execute(self, arguments):
        if arguments.package == None:
            for package in self.packageManager().getPackages(common.PackageManager.GET_PERMISSIONS | common.PackageManager.GET_CONFIGURATIONS | common.PackageManager.GET_GIDS | common.PackageManager.GET_SHARED_LIBRARY_FILES | common.PackageManager.GET_ACTIVITIES):
               self.__get_package(arguments, package) 
        else:
            package = self.packageManager().getPackageInfo(arguments.package, common.PackageManager.GET_PERMISSIONS | common.PackageManager.GET_CONFIGURATIONS | common.PackageManager.GET_GIDS | common.PackageManager.GET_SHARED_LIBRARY_FILES | common.PackageManager.GET_ACTIVITIES)
            self.__get_package(arguments, package)
            
    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest == "permission":
            return android.permissions

    def __get_package(self, arguments, package):
        application = package.applicationInfo
        activities = package.activities
        services = package.services
```

只要在 drozer console 中使用 `app.activity.info` 模块，就会调用 `execute()` 方法。

我们看到它调用了包管理器中的 API －－ `self.packageManager().getPackages(...)`。这个包返回一个带有各个包的权限、配置、GID，以及共享库的所有包对象的列表(list)。这个脚本对列表中的每个对象调用一次 `self.__get_package()` 函数，把它打印到 drozer console 的屏幕上。

### 枚举 activity

```sh
dz> run app.activity.info

dz> run app.activity.info --filter [activity name]
OR
dz> run app.activity.info -f [activity name]

dz> run app.activity.info --package [package name]
OR
dz> run app.activity.info -a [package name]
```

扩展阅读：<https://github.com/mwrlabs/drozer/blob/develop/src/drozer/modules/app/activity.py>

### 枚举 content provider

```sh
dz> run app.provider.info

dz> run app.provider.info --package [package name]
OR
dz> run app.provider.info -a [package name]

dz> run app.provider.info --permission [permission label]
OR
dz> run app.provider.info -p [permission label]
```

工作原理：<https://github.com/mwrlabs/drozer/blob/develop/src/drozer/modules/app/provider.py>

```py
    def execute(self, arguments):
        if arguments.package == None:
            for package in self.packageManager().getPackages(common.PackageManager.GET_PROVIDERS | common.PackageManager.GET_URI_PERMISSION_PATTERNS):
                self.__get_providers(arguments, package)
        else:
            package = self.packageManager().getPackageInfo(arguments.package, common.PackageManager.GET_PROVIDERS | common.PackageManager.GET_URI_PERMISSION_PATTERNS)

            self.__get_providers(arguments, package)


    def __get_providers(self, arguments, package):
        providers = self.match_filter(package.providers, 'authority', arguments.filter)        
        
        if arguments.permission != None:
            r_providers = self.match_filter(providers, 'readPermission', arguments.permission)
            w_providers = self.match_filter(providers, 'writePermission', arguments.permission)
            
            providers = set(r_providers + w_providers)
```

这个脚本通过调用 Android 包管理器，并传给它一些标志位提取出一个包的列表。我们看到，一旦包管理器收集到这些关于 `content proviser` 的详细信息后，脚本会调用一个名为 `__get_provider()` 方法，这个方法提取了 `provider` 的读和写的权限。`__get_provider()` 方法的作用基本上就是在定义了 `content provider` 权限的段中寻找一些字符串值，它调用 `math_filters()` 执行一些简单的字符串匹配，如果 `content provider` 所需的权限是读，这个字符串会被标上 `readPermission`；如果 `content provider` 所需权限是写，它会被标上 `writePermission`。之后，它会设置一个 provider 对象，然后把结果输出到 console 上。

扩展阅读：<https://developer.android.com/guide/topics/providers/content-providers.html>

### 枚举 service

```sh
dz> run app.service.info

dz> run app.service.info --package [package name]

dz> run app.service.info --permission [permission label]
OR
dz> run app.service.info -p [permission label]

dz> run app.service.info --filter [filter string]
OR
dz> run app.service.info -f [filter string]

dz> run app.service.info --unexported
OR
dz> run app.service.info -u
`` `

 works: 

```py
 def execute(self, arguments):
 if arguments.package == None:
 for package in self.packageManager().getPackages(common.PackageManager.GET_SERVICES | common.PackageManager.GET_PERMISSIONS):
 self.__get_services(arguments, package)
 else:
 package = self.packageManager().getPackageInfo(arguments.package , common.PackageManager.GET_SERVICES | common.PackageManager.GET_PERMISSIONS)

 self.__get_services(arguments, package)
```

This script will check whether a specific package needs to pass in an argument. If no argument is required, or the package name has already been Definition, this script will extract a list of packages, and in the loop, call the `self.__get_services()` method once for each package. When extracting the package list, according to the method `self.packageManager().getPackageInfo(arguments.package, common, PackageManager.GET_SERVICES | common.PackageManager.GET_PERMISSIONS)` The returned data is the result of string matching, and some attributes of the package can be filtered. 

Extended reading: 

- <https://github.com/mwrlabs/drozer/blob/develop/src/drozer/modules/app/service.py>
- <https://developer .android.com/guide/components/services.html>
- <https://developer.android.com/reference/android/app/Service.html>
- <https://developer.android.com/guide/components/bound-services.html>

### Enumerate broadcast receiver

```sh
dz> run app.broadcast.info% 0A
dz> run app.broadcast.info --package [package]
OR
dz> run app.broadcast.info -a [package]

dz> run app.broadcast.info --filter [filter]
OR
dz> run app.broadcast.info -f [filter]

dz> run app.broadcast.info --unexported
OR
dz> run app.broadcast .info -u
```

Extended reading:

- <https://developer.android.com/reference/android/content/BroadcastReceiver.html>
- <https://github.com/mwrlabs/drozer/blob/develop/src/drozer/modules/app/broadcast .py>

### Determine the attack surface of the app

an app 的受攻击面就是它导出组件的数量。

```sh
dz> run app.package.attacksurface [package name]
```

工作原理：
<https://github.com/mwrlabs/drozer/blob/develop/src/drozer/modules/app/package.py>

```py
from drozer import android
from drozer.modules import common, Module
class AttackSurface(Module, common.Filters, common.PackageManager):

    def execute(self, arguments):
        if arguments.package != None:
            package = self.packageManager().getPackageInfo(arguments.package, common.PackageManager.GET_ACTIVITIES | common.PackageManager.GET_RECEIVERS | common.PackageManager.GET_PROVIDERS | common.PackageManager.GET_SERVICES)
            application = package.applicationInfo

            activities = self.match_filter(package.activities, 'exported', True)
            receivers = self.match_filter(package.receivers, 'exported', True)
            providers = self.match_filter(package.providers, 'exported', True)
            services = self.match_filter(package.services, 'exported', True)
            
            self.stdout.write("Attack Surface:\n")
            self.stdout.write("  %d activities exported\n" % len(activities))
            self.stdout.write("  %d broadcast receivers exported\n" % len(receivers))
            self.stdout.write("  %d content providers exported\n" % len(providers))
            self.stdout.write("  %d services exported\n" % len(services))

            if (application.flags & application.FLAG_DEBUGGABLE) != 0:
                self.stdout.write("    is debuggable\n")

            if package.sharedUserId != None:
                self.stdout.write("    Shared UID (%s)\n" % package.sharedUserId)
        else:
            self.stdout.write("No package specified\n")
```

这个模块会通过包管理器 API 提取关于 `service`、`activity`、`broadcast receiver` 和 `content provider` 的信息，然后根据得到的信息，确定它们是不是被导出。

### 运行 activity

1. 寻找一些 activity

```sh
dz> run app.activity.info --package [package name]
```

2. 发送如何运行的 intent

```sh
dz> run app.activity.start --action [intent action] --category [intent category] --component [package name] [component name]

dz> run app.activity.forintent --action [intent action] -category [intent category]
```

How it works:
<https://raw.githubusercontent.com/mwrlabs/drozer/develop/src/drozer/modules/app/activity.py>

` ``py
 def execute(self, arguments):
 intent = android.Intent.fromParser(arguments)

 if len(intent.flags) == 0:
 intent.flags.append('ACTIVITY_NEW_TASK')
 
 if intent.isValid():
 self.getContext().startActivity(intent.buildIn(self))
 else:
 self. stderr.write("invalid intent: one of action or component must be set\n")
```

drozer Put the user-input parameters obtained through the parameter parser into an `intent`, check whether they are valid, and send them out. 

Extended reading: 

- <https://developer.android.com/reference/android/content/Intent.html>
- <https://developer.android.com/guide/components /intents-filters.html>
- <https://developer.android.com/guide/components/activities.html>

Writing extensions: 

- <https://developer.android.com/reference/android/os/Build.html>
- <https://github.com/mwrlabs/drozer/wiki/Writing-a-Module>

# # Chapter 4 Exploiting Vulnerabilities in App

### Collect information leaked by logcat

```sh
adb logcat [options] [filter]

adb logcat > output.txt

adb logcat | grep [pattern]
```

Android's Monkey testing framework is used to send system/hardware-level events to the app. 

```sh
adb shell monkey -p [package] -v [event count]
```

Extended reading: 

- <https://developer.android.com /studio/command-line/logcat.html>
- <http://blog.parse.com/learn/engineering/discovering-a-major-security-hole-in-facebooks-android-sdk/>
- <https://developer.android.com/studio/ command-line/adb.html#logcat>
- <http://www.vogella.com/tutorials/AndroidTesting/article.html>

### Check the network traffic

After confirming that tcpdump and netcat have been installed on the Android device, you can capture the network traffic

```sh
tcpdump -w - | nc -l -p 31337
```
 
 passes the output of tcpdump to Wireshark on the local computer, first through ADB Set up port forwarding 

```sh
adb forward tcp:12345 tcp:31337
```

 and finally transfer the output to Wireshark through the pipeline

```sh
./ adb forward tcp:12345 tcp:31337 && netcat 127.0.0.1 12345 | wireshark -k -S -i -
```

Extended reading:

- <https://code.tutsplus.com/tutorials/analyzing-android-network-traffic--mobile-10663>
- <https://wiki.wireshark.org/DisplayFilters>
- <https:// wiki.wireshark.org/CaptureFilters>
- <http://www.tcpdump.org/tcpdump_man.html>
- <https://www.wireshark.org/docs/wsug_html_chunked/>

### Attack service

1. For a given app, find which services are exported

```sh 
dz> run app.service.info --permission null
```

2. Found a bunch of services After that, run them using the following command

```sh
dz> run app.service.start --action [ACTION] --category [CATEGORY] --data-uri [DATA-URI] --component [ package name] [component name] --extra [TYPE KEY VALUE] --mimetype [MIMETYPE]
```

When stopping and starting these services, they can run at the same time `logcat`. 

3. Basically, look for the following part in the XML file

```sh
<action
<meta-data
```

4. In order to send the intent to For this service, you can execute the command

```sh
// Take `com.linkedin.android` as an example
dz> run app.service.start in drozer console --component com.linkedin.android com.linkedin.android.authenticator.AuthenitactionService --action android.accounts.AccountAuthenitcator
```

Extended reading:
<https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2011-4276&cid=6>
 
### Attack broadcast receiver

 Pay special attention to the `intent filter` in the broadcast receiver when reading the source code of the vulnerability. definition. 

Send an intent

```sh
dz> run app.broadcast.send --action [ACTION] --category [CATEGORY] --component [PACKAGE COMPONENT] --data- uri [DATA-URI] -extra [TYPE KEY VALUE] -flags [FLAGS*] -mimetype [MIMETYPE]
```

Extended reading:

- <http://www.cs.wustl.edu/~jain/cse571-11/ftp/trojan/index.html>
 - <https://blog.lookout.com/blog/2010/08/10/security-alert-first-android-sms-trojan-found-in-the-wild/>

### The enumeration has Vulnerable content provider

1. Enumerate content provider

```sh
dz> run app.provider.info --permission that does not require permission null
```

2. After selecting a content provider, list all URIs with host names

```sh
dz> run app.provider.finduri [package]
`` `

 How it works:

```py
 def findContentUris(self, package):
 """
 Search a package for content providers, by looking for content:// paths
 in the binary.
 """

 self.deleteFile("/".join([self.cacheDir(), "classes.dex"]))

 content_uris = []
 for path in self.packageManager().getSourcePaths(package):
 strings = []

 if ".apk" in path:
 dex_file = self.extractFromZip("classes.dex", path, self.cacheDir())

 if dex_file != None:
 strings = self.getStrings(dex_file.getAbsolutePath())

 dex_file.delete()
 
 # look for an odex file too, because some system packages do not
 # list these in sourceDir
 strings += self .getStrings(path.replace(".apk", ".odex")) 
 elif (".odex" in path):
 strings = self.getStrings(path)
 
 content_uris.append((path, filter(lambda s: ("CONTENT://" in s.upper()) and ("CONTENT:// " != s.upper()), strings)))

 return content_uris
```

`.finduri` module lists all possible contents URI method: Open the app's DEX file and directly look for strings in the unparsed file that look like valid content URI formats. 

Extended reading: 

- <https://github.com/mwrlabs/drozer/blob/develop/src/drozer/modules/common/provider.py>
- <https://github .com/mwrlabs/drozer/blob/develop/src/drozer/modules/app/provider.py>
- <https://developer.android.com/guide/topics/security/permissions.html#uri>
- <https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2013 -2318&cid=3>

### Extract data

1 from the vulnerable content provider. Get the vulnerable content provider

```sh
run app.provider.info --permission null
run app.provider.finduri [package]
```

2. Extract and download data

`` `sh
dz> run app.provider.query [URI]
dz> run app.provider.download [URI]
```

Extended reading:

- <http://www.cvedetails.com/cve/CVE-2010-4804/>
- <http://vuln. sg/winzip101-en.html>

### Insert data 

1 into the content provider. List the data structure and column names and other information

```sh
dz> run app.provider.columns [URI]
```

2. Insert data

`` `sh
dz> run app.provider.insert [URI] [--boolean [name] [value]] [--integer [name] [value]] [--string [name] [value]]...
```

### Enumerate content providers with SQL injection vulnerabilities

```sh
dz> run app.provider.query [URI] -- selection "1=1"
dz> run app.provider.query [URI] --selection "1-1=0"
...
```

Extended reading:

- <http://www.sqlite.org/lang.html>
- <https://www.owasp.org/index.php/SQL_Injection>

### Use the debuggable app

1. To check whether an app is debuggable, you can directly view the manifest, you can also execute

```sh
dz> run app.package.debuggable
```

2. Run

```sh
dz> run app.activity.start --component com.example.readmycontacts com.example.readmycontacts.MainActivity
```

3. You can use ADB Connect to the java debugging connection protocol port, which is a port opened on the virtual machine instance specifically for debugging, and returns the interface that can be connected to the VM

```sh
adb jdwp
```

4 . Use ADB to forward port

```sh
adb forward tcp:[localport] jdwp:[jdwp port on device]
```

5. Use the Java debugger to connect to VM

```sh
jdb -attach localhost:]PORT]
```

6 from the local computer. Extract Class information

```sh
classes
```

7. Enumerate all methods in the specified class

```sh
> methods [class-path]
```

8. List the names and values ​​of the fields or class attributes of the class, execute

```sh
> fields [class name]
 in jdb ```

Extended reading:

- <http://docs.oracle.com/javase/1.5.0/docs/tooldocs/windows/jdb.html>
- <http://docs.oracle.com/javase/1.5.0/docs/guide/jpda/index.html>
- <https://developer.android.com/guide/topics/manifest/application-element .html#debug>
- <https://labs.mwrinfosecurity.com/blog/debuggable-apps-in-android-market>
- <http://www.saurik.com/id/17>
- <https://www.packtpub.com/books/content/debugging-java-programs-using-jdb>
- <https:/ /android.googlesource.com/platform/dalvik/+/gingerbread-release/vm/jdwp/JdwpAdb.c>
- <https://android.googlesource.com/platform/dalvik/+/eclair-passion-release/vm/jdwp/JdwpAdb.c>
- <https://android.googlesource.com/platform/dalvik/+ /kitkat-release/vm/jdwp/JdwpAdb.cpp>

## Chapter 5 Protecting app

### Contains app There are two methods for the component

: one is to use the `AndroidManifest.xml` file correctly, and the other is to force permission checking at the code level. 

If a component does not need to be called by other apps, or needs to be clearly isolated from other components, add the following attribute

```sh
<[component name] to the XML element of the component android:exported="false">
</[component name]>
```

Extended reading:

- <https://developer.android.com/guide/topics/manifest/service-element.html>
- <https://developer.android.com/guide/topics/manifest/receiver-element.html>% 0A- <https://developer.android.com/guide/topics/manifest/activity-element.html>
- <https://developer.android.com/guide/topics/manifest/application-element.html>
- <https://developer.android.com/guide/topics/manifest/manifest-intro.html>
- <https://developer.android.com/reference/android/content/Context.html>
- <https://developer.android.com/reference/android/app/Activity.html>

### Protect component 

1 with custom permissions. Statement stated String of `permission` label, edit `res/values/strings.xml` file

```sh
<string name="custom_permission_label">Custom Permission</string>
```
 
2. Add a custom permission with a protection level of `normal` and add the following string 

```sh
<permission in the `AndroidManifest.xml` file android:name="android.permission.CUSTOM_PERMISSION"
 android:protectionLevel="normal"
 android:description="My custom permission"
 android:label="@string/custom_permission_label">
```% 0A
3. Add it to the `android:permission` attribute of a component in the app

```sh
<activity ...
 android:permission="android.permission.CUSTOM_PERMISSION">
</activity>
```

 can also be `provider`, `service`, `receiver`. 

4. You can also add the tag 

```sh
<uses-permission android:name="android.permission.CUSTOM_PERMISSION"/>
` in the `AndroidManifest.xml` file of other apps. ``

Define permission group: 

1. In `res/values/string.xml` Add a string representing the permission group label

```sh
<string name="my_permissions_group_label">Personal Data Access</string>
```

2. In AndroidManifest.xml Add code

```sh
<permission-group
 android:name="android.permissions.persomal_data_access_group"
 android:label="@string/my_permissions_group_label"
 android:description="Permissions that allow access to personaldata" />
```

3. Assign the defined permissions to the group

`` `sh
<permission ...
 android:permissionGroup="android.permission.personal_data_access_group" />
```

Extended reading:

- <https://developer.android.com/guide/topics/manifest/permission-element.html>
- <https:// developer.android.com/guide/topics/manifest/uses-permission-element.html>
- <https://developer.android.com/guide/topics/manifest/permission-group-element.html>
- <https://developer.android.com/reference/android/Manifest.permission.html>% 0A
### Protect content provider paths

1. Set a permission to manage read and write permissions for all paths related to your authentication, in `manifest` Add the following element where `[permission name]` is the permission that other apps must have to read or write any content provider path. 

```sh
<provider android:enabled="true"
 android:exported="true"
 android:authorities="com.android.myAuthority"
 android:permission="com.myapp.provider"
 android:permission="[ permission name]">
</provider>
```

2. Add read and write permissions. 

```sh
<provider
 android:writePermission="[write permission name]"
 android:readPermission="[read permission name]">
</provider>
``` 

Extended reading:

- <https://developer.android.com/guide/topics/manifest/provider-element.html>
- <https://developer.android.com/guide/topics/manifest/path-permission-element.html>

### Defense against SQL injection attacks

1. When instantiating a RssItemDAO object, insertStatement The object is compiled into a parameterized SQL insert statement string

```java
public class RssItemDAO {

private SQLiteDatabase db;
private SQLiteStatement insertStatement;

private static String COL_TITLE = "title";
private static String TABLE_NAME = "RSS_ITEMS";

private static String INSERT_SQL = "insert into " + TABLE_NAME + " (content, link, title) values ​​(?,?,?)";

public RssItemDAO(SQLiteDatabase db) {
 this.db = db;
 insertStatement = db.compileStatement(INSERT_SQL);
}
```

2. When inserting a new RssItem object into the database, You can bind each attribute

```java
public long save(RssItem item) in the order they appear in the statement. {
 insertStatement.bindString(1, item.getContent());
 insertStatement.bindString(2, item.getLink());
 insertStatement.bindString(3, item.getTitle());
 return insertStatement .executeInsert();
}
```

3. Shows how to use SQLiteDatabase.query To get RssItems

```java
public List<RssItem> fetchRssItemsByTitle(String searchTerm) {
 Cursor cursor = db.query(TABLE_NAME, null, COL_TITLE + "LIKE ?", new String[] { "%" + searchTerm + "%" }, null, null, null);
 // process cursor into list
 List<RssItem> rssItems = new ArrayList<RssItemDAO.RssItem>();
 cursor.moveToFirst();
 while (!cursor.isAfterLast()) {% 0A // maps cursor columns of RssItem properties
 RssItem item = cursorToRssItem(cursor);
 rssItems.add(item);
 cursor.moveToNext();
 }
 return rssItems;
}
```

Extended reading: 

- <https://developer.android.com/reference/android/database/sqlite/SQLiteDatabase.html>
- <https://developer.android.com/reference/android/database/sqlite/SQLiteStatement.html>% 0A- <https://www.owasp.org/index.php/Query_Parameterization_Cheat_Sheet>
- <http://www.sqlite.org/lang_expr.html>

### Verify the app’s signature

 to ensure there is a signature private key. If not, use the following method to create

` ``sh
keytool -genkey -v -keystore your_app.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
```

1. Find the SHA1 signature of your certificate

```sh
keytool -list -v -keystore your_app.keystore

// for example
71:92:0A:C9:48:6E:08:7D:CB:CF:5C:7F:6F:EC:95:21:35:85:BC:C5 :
```
% 0A2. Copy the hash into the app. In the Java `.class` file, remove the colon and define it as a static string 

```sh
private static String CERTIFICATE_SHA1 = "71920AC9486E087DCBCF5C7F6FEC95213585BCC5";
```

3. Write code to obtain the current signature of the .apk file at runtime

```java
public static boolean validateAppSignature(Context context) {% 0A try {
 // get the signature form the package manager
 PackageInfo packageInfo = context.getPackageManager().getPackageInfo(context.getPackageName(), PackageManager.GET_SIGNATURES);
 Signature[] appSignatures = packageInfo.signatures;
 
 //this sample only checks the first certificate
 for (Signature signature : appSignatures) {
 byte[] signatureBytes = signature.toByteArray();
 //calc sha1 in hex
 String currentSignature = calcSHA1(signatureBytes);
 //compare signatures
 return CERTIFICATE_SHA1.equalsIgnoreCase(currentSignature);
 }
 } catch ( Exception e) {
 // if error assume failed to validate
 }
 return false;
}
```

4. Save the signature hash and convert it into hexadecimal

```java
private static String calcSHA1(byte[] signature) throws NoSuchAlgorithmException {
 MessageDigest digest = MessageDigest.getInstance("SHA1");
 digest.update(signature);
 byte[] signatureHash = digest.digest();
 return bytesToHex(signatureHash);
}
public static String bytesToHex(byte[] bytes) {
 final char[] hexArray = { '0', '1', '2 ', '3', '4', '5', '6', '7', '8','9', 'A', 'B', 'C', 'D', 'E', 'F' };% 0A char[] hexChars = new char[bytes.length * 2];
 int v;
 for (int j = 0; j < bytes.length; j++) {
 v = bytes[j] & 0xFF;
 hexChars[j * 2] = hexArray[v >>> 4];
 hexChars[j * 2 + 1] = hexArray[v & 0x0F];
 }
 return new String(hexChars); 
}
```

5. Compare

```sh
CERTIFICATE_SHA1.equalsIgnoreCase(currentSignature);
```

Extended reading:

- <https://developer.android.com/studio/publish/app -signing.html>
- <https://gist.github.com/scottyab/b849701972d57cf9562e>
- <https://developer.android.com/reference/android/content/pm/Signature.html>
- <https://developer .android.com/reference/android/content/pm/PackageManager.html>
- <http://www.saurik.com/id/17>
- <http://docs.oracle.com/javase/6/docs/technotes/tools/windows/keytool.html>

# ## Anti-reverse engineering

1 by detecting the installer, emulator, and debugging flags. Check whether the installer is the Google Play Store

```java
public static boolean checkGooglePlayStore(Context context) {
 String installerPackageName = context.getPackageManager().getInstallerPackageName(context.getPackageName());
 return installerPackageName != null && installerPackageName.startsWith("com.google.android");
} 
```

2. Check whether it is running in an emulator

```java
public static boolean isEmulator() {
 try {
 Class systemPropertyClazz = Class.forName("android.os.SystemProperties");
 boolean kernelQemu = getProperty(systemPropertyClazz, "ro.kernel.qemu").length() > 0;
 boolean hardwareGoldfish = getProperty(systemPropertyClazz, "ro.hardware").equals("goldfish");
 boolean modelSdk = getProperty(systemPropertyClazz, "ro.product.model").equals("sdk");
 
 if ( kernelQemu || hardwareGoldfish || modelSdk) {
 return true;
 }
 } catch (Exception e) {
 // error assumes emulator
 }
 return false;
}

private static String getProperty(Class clazz, String propertyName) throws Exception {
 return (String) clazz.getMethod( "get", new Class[] { String. class }).invoke(clazz, new Object[] { propertyName });
}
```

3. Check whether the debuggable flag is turned on

```java
public static boolean isDebuggable(Context context){
 return (context.getApplicationInfo().flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0;
}% 0A```

Extended reading:

- <https://github.com/android/platform_frameworks_base/blob/master/core/java/android/os/SystemProperties.java>
- <https://developer.android.com/reference/android/content/pm /PackageManager.html>
- <https://developer.android.com/reference/android/content/pm/ApplicationInfo.html>

### Using ProGuad

1. Under Android Studio, you need to add the following code to the release part of `buildType` in the Gradle Build system

```sh
android {
...
 buildTypes {
 release { 
 runProguard true
 proguardFile file('../proguard-project.txt)
 proguardFile getDefaultProguardFile('proguard-android.txt')
 }
 }
}
```

2. Ensure that the `proGuard-android.txt` file is always in the location specified in the configuration. 

Extended reading: 

- <https://developer.android.com/studio/build/shrink-code.html>
- <https://sourceforge.net/projects/proguard/> 
- <http://proguard.sourceforge.net/index.html#manual/examples.html>

## Chapter 6 Reverse engineering app

### Put Java The source code is compiled into a DEX file

1. Open the text editor and create a file

```java
public class Example{
 public static void main(String []args){
 System.out. printf("Hello World!\n");
 }
}
```

2. Compile to get .class File

```sh
javac -source 1.6 -target 1.6 Example.java
```

3. Use dx to get a DEX file

```sh
/sdk/build -tools/25.0.0/dx --dex --output=Example.dex Example.class
```

### Parse DEX File format

<https://github.com/android/platform_dalvik/blob/master/libdex/DexFile.h>

DEX file format:

```c
struct DexFile {% 0A /* directly-mapped "opt" header */
 const DexOptHeader* pOptHeader;

 /* pointers to directly-mapped structs and arrays in base DEX */
 const DexHeader* pHeader;
 const DexStringId* pStringIds;
 const DexTypeId* pTypeIds;
 const DexFieldId* pFieldIds;
 const DexMethodId* pMethodIds;
 const DexProtoId* pProtoIds;
 const DexClassDef* pClassDefs;
 const DexLink* pLinkData;

 /*
 * These are mapped out of the "auxillary" section, and may not be
     * included in the file.
     */
    const DexClassLookup* pClassLookup;
    const void*         pRegisterMapPool;       // RegisterMapClassPool

    /* points to start of DEX file data */
    const u1*           baseAddr;

    /* track memory overhead for auxillary structures */
    int                 overhead;

    /* additional app-specific data structures associated with the DEX */
    //void*               auxData;
};
```

下面我们分别来分析各个区段：

DEX 文件头：

```c
struct DexHeader {
    u1  magic[8];           /* includes version number */
    u4  checksum;           /* adler32 checksum */
    u1  signature[kSHA1DigestLen]; /* SHA-1 hash */
    u4  fileSize;           /* length of entire file */
    u4  headerSize;         /* offset to start of next section */
    u4  endianTag;
    u4  linkSize;
    u4  linkOff;
    u4  mapOff;
    u4  stringIdsSize;
    u4  stringIdsOff;
    u4  typeIdsSize;
    u4  typeIdsOff;
    u4  protoIdsSize;
    u4  protoIdsOff;
    u4  fieldIdsSize;
    u4  fieldIdsOff;
    u4  methodIdsSize;
    u4  methodIdsOff;
    u4  classDefsSize;
    u4  classDefsOff;
    u4  dataSize;
    u4  dataOff;
};
```

```c
/*
 * These match the definitions in the VM specification.
 */
typedef uint8_t             u1;
typedef uint16_t            u2;
typedef uint32_t            u4;
typedef uint64_t            u8;
typedef int8_t              s1;
typedef int16_t             s2;
typedef int32_t             s4;
typedef int64_t             s8;
```

StringIds 区段：

由一系列相对 DEX 文件的加载基地址的偏移量组成，用于计算定义在 Data 区段中的各个静态字符串的起始位置。

```c
struct DexStringId {
    u4 stringDataOff;      /* file offset to string_data_item */
};
```

编译器、反编译器、虚拟机如何寻找字符串：

```c
/* return the const char* string data referred to by the given string_id */
DEX_INLINE const char* dexGetStringData(const DexFile* pDexFile,
        const DexStringId* pStringId) {
    const u1* ptr = pDexFile->baseAddr + pStringId->stringDataOff;

    // Skip the uleb128 length.
    while (*(ptr++) > 0x7f) /* empty */ ;

 return (const char*) ptr;
}
```

TypeIds section: stores the information needed to find the corresponding string for each type. 

```c
struct DexTypeId {
 u4 descriptorIdx; /* index into stringIds list for type descriptor */
};
```

ProtoIds section: stores a series of descriptions The prototype ID of the method, which contains information about the return type and parameters of each method. 

```c
struct DexProtoId {
 u4 shortyIdx; /* index into stringIds for shorty descriptor */
 u4 returnTypeIdx; /* index into typeIds list for return type */
 u4 parametersOff; /* file offset to type_list for parameter types */
};
```

FieldIds Section: It consists of the index number of the data in the StringIds and TypeIds sections, describing each member of the class. 

```c
struct DexFieldId {
 u2 classIdx; /* index into typeIds list for defining class */
 u2 typeIdx; /* index into typeIds for field type */
 u4 nameIdx; /* index into stringIds for field name */
};
```

MethodIds Section: 

```c
struct DexMethodId {
 u2 classIdx; /* index into typeIds list for defining class */
 u2 protoIdx; /* index into protoIds for method prototype */
 u4 nameIdx ; /* index into stringIds for method name */
};
```

ClassDefs Section: 

```c
struct DexClassDef {
 u4 classIdx; /* index into typeIds for this class */
 u4 accessFlags;
 u4 superclassIdx; /* index into typeIds for superclass */% 0A u4 interfacesOff; /* file offset to DexTypeList */
 u4 sourceFileIdx; /* index into stringIds for source file name */
 u4 annotationsOff; /* file offset to annotations_directory_item */
 u4 classDataOff; /* file offset to class_data_item */
 u4 staticValuesOff; /* file offset to DexEncodedArray */
}; 
```

 Below we use the dexdump tool to analyze DEX: 

```sh
/sdk/build-tools/25.0.0/dexdump Example.dex
```

 You can also use the dx tool, which is closer to the DEX file format. Parsing: 

```sh
dx --dex --verbose-dump -dump-to=[output-file].txt [input-file].class
```

Extended reading:

- <http://retrodev.com/android/dexformat.html>
- <https://github.com /JesusFreke/smali>
- <http://www.strazzere.com/papers/DexEducation-PracticingSafeDex.pdf>
- <https://github.com/android/platform_dalvik/tree/master/libdex>
- <http://source .android.com/devices/tech/dalvik/dex-format.html>

### Interpretation of Dalvik bytecode

 using baksmali The tool decompiles DEX files into well-formatted smali files. 

```sh
baksmali [dex filename].dex
```

Extended reading: 

- <http://source.android.com/devices/tech/dalvik/ instruction-formats.html>
- <http://source.android.com/devices/tech/dalvik/dalvik-bytecode.html>

### Put DEX Decompile back to Java

1. Use the Dex2jar tool to convert the DEX file into a .class file

```sh
dex2jar [dex file].dex
```

2. Use jd-gui The tool obtains the source file

### and decompiles the objdump provided in the toolchain of the app's native library

Android NDK. 

```sh
objdump -D [native library].so
```

Extended reading: 

- <http://www.atmel.com/Images/DDI0029G_7TDMI_R3_trm. pdf>
- <http://infocenter.arm.com/help/topic/com.arm.doc.ihi0044f/IHI0044F_aaelf.pdf>
- <http://www.arm.com/products/processors/instruction-set-architectures /index.php>
- <http://refspecs.linuxbase.org/elf/elf.pdf>

### Use GDB server to debug Android Process 

1. Make sure gdbserver is installed on the device, and then view all running processes

```sh
ps
```

2. After getting a valid PID, use gdbserver to attach It

```sh
gdbserver:[tcp-port number] --attach [PID]
```

3. Perform port forwarding on the local computer

```sh
adb forward tcp:[device port-number] tcp:[local port-number]
` ``

4. After running gdb (NDK toolchains)

```sh
target remote :[PID]
```

## Chapter 7 Network Security

- <https://developer.android.com/training/articles/security-ssl.html>
- < http://www.bouncycastle.org/latest_releases.html>
- <https://developer.android.com/reference/javax/net/ssl/HttpsURLConnection.html>
- <https://developer.android.com/reference/javax/net/ssl/SSLSocketFactory.html>% 0A- <https://guardianproject.info/code/onionkit/>
- <https://play.google.com/store/apps/details?id=org.torproject.android>
- <https://code.google.com/archive/p/httpclientandroidlib/>
- < https://github.com/guardianproject/cacert>
- <https://www.owasp.org/index.php/Man-in-the-middle_attack>
- <https://www.madboa.com/geek/openssl/>
- <https://www.owasp.org/index.php/Certificate_and_Public_Key_Pinning>
- <https://github.com/moxie0/AndroidPinning>
- <https://www.imperialviolet.org/2011/05/04/pinning.html>

## Chapter 8 Vulnerabilities in Native Code Utilization and analysis

### Check file permissions

First install the busybox tool. 

 List files readable by all users: 

```sh
./busybox find [path-to-search] -perm 0444 -exec ls -al {} \;
` ``

File writable by all users: 

```sh
./busybox find [path-to-search] -perm 0222 -exec ls -al {} \;
```

File executable by all users: 

```sh
./busybox find [path-to-search] -perm 0111 -exec ls -al {} \;
```

 If you want to find files in which the specified bit is set to 1 and it doesn't matter if other bits are set or not, you can add a `"-"` in front of the search permission parameter. symbol as a prefix. 

Find executable files with the setuid bit set to 1: 

```sh
./busybox find [path-to-search] -perm -4111 -exec ls -al {} \ ;
```

Find files with all setguid bits and executable bits set to 1:

```sh
./busybox find [path-to-search] -perm -2111 -exec ls -al {} \;
```

Find all files belonging to the root user: 

```sh
./ busybox find [path-to-search] -user 0 -exec ls -al {} \;
```

Find the files of all system users: 

```sh
./ busybox find [path-to-search] -user 1000 -exec ls -al {} \;
```

List files according to group ID: 

```sh
./busybox find [path-to-search] -group 0 -exec ls -al {} \;
```

 Create a list of UIDs for each app: 

```sh
ls -al /data/data/
```

We see that the naming format of the app is `u[number]_a[number]`, which specifically means `u[user profile number]_a[ID]`, Add 10000 to the `ID` to get the `UID` actually used in the system. 

Find all files of the user with this UID:

```sh
./busybox find /data/data/ -user [UID] -exec ls -al {} \;
` ``

Extended reading:

- <https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2009-1894>
- <https://android.googlesource.com/platform/system/core/+/android -4.4.2_r1/include/private/android_filesystem_config.h>
- <http://www.tldp.org/HOWTO/HighQuality-Apps-HOWTO/fhs.html>
- <http://www.pathname.com/fhs/pub/fhs-2.3.pdf>
% 0A### Cross-compile native executable programs

 using the Android native development kit (NDK). 

1. Create a directory for the code, such as "buffer-overflow". A subdirectory named `jni` must be created in this directory, because the NDK compilation script will specifically look for this directory. 
2. Create an Android.mk file in the JNI directory and record some compilation-related attributes. 

```sh
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
# give module name
LOCAL_MODULE := buffer-overflow #name of folder
# list your C files to compile
LOCAL_SRC_FILES := buffer-overflow.c #name of source to compile
# this option will build executables instead of building library for Android application.
include $(BUILD_EXECUTABLE)
```

3. Sample code, saved in In the jni directory: 

```c
#include<stdio.h>
#include<string.h>
void vulnerable(char *src) {
 char dest[10];
 strcpy (dest, src);
 printf("[%s]\n", dest);
 return;
}
void call_me_maybe() {
 printf("so much win!!\n");
 return;
}
int main(int argc, char **argv) {
 vulnerable(argv[1]);% 0A return 0;
}
```

4. Call NDK build The script is compiled

```sh
[path-to-ndk]/ndk-build
```

5. Use objdump of NDK specific version Parse the assembly code of this executable file

```sh
[path-to-ndk]/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/arm-linux-androideabi- objdump -D buffer-overflow/obj/local/armeabi/buffer-overflow > buffer-overflow.txt
```

Extended reading:

- <http://infocenter.arm.com/help/topic/com.arm.doc.qrc0001l/QRC0001_UAL.pdf>% 0A- <http://simplemachines.it/doc/arm_inst.pdf>
- <http://101.96.8.164/web.eecs.umich.edu/~prabal/teaching/eecs373-f10/readings/ARMv7-M_ARM.pdf>
- <https://www.exploit-db.com/ docs/16151.pdf>
- <http://101.96.8.165/infocenter.arm.com/help/topic/com.arm.doc.ihi0042e/IHI0042E_aapcs.pdf>
- <https://www.exploit-db.com/docs/16151 .pdf>
- <http://infocenter.arm.com/help/topic/com.arm.doc.ihi0042f/IHI0042F_aapcs.pdf>
- <http://infocenter.arm.com/help/topic/com.arm.doc .dui0068b/DUI0068.pdf>
- <https://android.googlesource.com/platform/bionic/>
- <https://android.googlesource.com/platform/bionic/+/jb-mr0-release/libc/bionic/dlmalloc.c>

### Exploiting vulnerabilities caused by race conditions

 Race conditions The problem arises due to the lack of enforced mutual exclusion conditions when processes run in multi-threaded systems that use a preemptive process scheduling system. Preemptive scheduling allows the task scheduler to forcefully interrupt a running thread or process. 

 To exploit a race condition vulnerability, at least the following conditions must be met:

1. Access to the resources that the vulnerable process competes for access to
2. Maliciously change these resources
3. Time of use/check time (TOU/ TOC) window size 

 Let’s prepare an example first, using Jelly Bean Simulator: 

```c
#include<stdio.h>
#include<unistd.h>
#include<errno.h>
#define MAX_COMMANDSIZE 100
int main(int argc , char *argv[], char **envp) {
 char opt_buf[MAX_COMMANDSIZE];
 char *args[2];
 args[0] = opt_buf;
 args[1] = NULL;
 int opt_int;
 const char *command_filename = "/data/race- condition/commands.txt";
 FILE *command_file;
 printf("option: ");
 opt_int = atoi(gets(opt_buf));
 printf("[*] option %d selected...\n", opt_int);
 if (access(command_filename, R_OK|F_OK) == 0) {
 printf("[*] access okay...\n");
 command_file = fopen(command_filename, "r");
 for (; opt_int>0; opt_int--) {
 fscanf(command_file, "%s", opt_buf);
 }
 printf("[*] executing [%s]...\n", opt_buf);
 fclose(command_file);
 }
 else {
 printf("[x] access not granted...\ n");
 }
 int ret = execve(args[0], &args, (char **)NULL);
 if (ret != NULL) {
 perror("[x] execve");
 }
 return 0;
}
```

1. Compile by cross-compiling the native executable program and deploy it to the Android device. It is placed in a directory on the system that any user has read and execute permissions. 
2. Create a new `race-condition` folder under `/data/` and put the `command.txt` file into it. 
3. After copying it to the device, give the executable file `setuid` permissions so that any user has execute permissions on the file. 

```sh
chmod 4711 /system/bin/race-condition
```

4. Log in with `ADB shell` and try to access some files that do not have execution, read or write permissions. The root file obviously cannot

5. We use the `race-condition` executable file and first go to `commands.txt` File writing command

```sh
echo "/system/bin/sh" >> /data/race-condition/commands.txt
```

 command is written to the last line , you can use `cat [filename]` to view the file and note which line the command just written is. 

6. Execute `race-condition` and enter the line number when asked for `option`. The vulnerable binary executable will execute the `sh` command and give you `root` privileges. 

Extended reading: 

- <https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2013-1727&cid=8>
- <https://web .nvd.nist.gov/view/vuln/detail?vulnId=CVE-2013-1731&cid=8>
- <https://packetstormsecurity.com/files/122145/Sprite-Software-Android-Race-Condition.html>
- <http://www.wright.edu/static/cats/maint/maintenance.html>% 0A
### Exploitation of stack overflow vulnerability

- <https://www.exploit-db.com/docs/24493.pdf>
- <http://phrack.org/issues/49/14.html#article>
- <http://thinkst.com/stuff/bh10/BlackHat-USA-2010-Meer-History-of-Memory-Corruption -Attacks-wp.pdf>
- <http://cseweb.ucsd.edu/~hovav/dist/noret-ccs.pdf>
- <https://www.informatik.tu-darmstadt.de/fileadmin/user_upload/Group_TRUST/PubsPDF/ROP-without-Returns-on-ARM.pdf>

### Automatic fuzzing test Android native code
 
- <http://www.linuxjournal.com/article/10844>
- <https://code.google.com/archive/p/ouspg/wikis/Radamsa.wiki>
- <https://code.google.com/archive/p/ouspg/wikis/Blab.wiki>% 0A- <http://gcc.gnu.org/onlinedocs/gcc/Code-Gen-Options.html>
- <http://www.cs.tut.fi/tapahtumat/testaus12/kalvot/Wieser_20120606radamsa-coverage.pdf >

## Chapter 9 Encryption and using device management policies during development

- <https://www.owasp.org/index.php/Using_the_Java_Cryptographic_Extensions>
- <http://rtyley.github.io/spongycastle/#downloads>
- <http://www.bouncycastle.org/ java.html>
- <http://cs.ucsb.edu/~yanick/publications/2013_ccs_cryptolint.pdf>
- <https://developer.android.com/reference/java/security/SecureRandom.html>
- <https: //developer.android.com/reference/javax/crypto/KeyGenerator.html>
- <http://www.openhandsetalliance.com/oha_members.html>
- <https://developer.android.com/reference/android/content/SharedPreferences.html>
- <http://www.codeproject .com/Articles/549119/Encryption-Wrapper-for-Android-SharedPreferences>
- <https://github.com/scottyab/secure-preferences>
- <https://github.com/commonsguy/cwac-prefs>
- <https://developer.android.com/reference/javax /crypto/SecretKeyFactory.html>
- <https://developer.android.com/reference/javax/crypto/spec/PBEKeySpec.html>
- <http://docs.oracle.com/javase/6/docs/technotes/guides/security/crypto/CryptoSpec.html>
- <http://android-developers.blogspot.co.uk/2013/02 /using-cryptography-to-store-credentials.html>
- <https://github.com/nelenkov/android-pbe>
- <https://www.zetetic.net/sqlcipher/buy/>
- <https://github.com/sqlcipher/android-database-sqlcipher>
- <https://guardianproject.info/code/ iocipher/>
- <https://developer.android.com/reference/java/security/KeyStore.html>
- <https://developer.android.com/samples/BasicAndroidKeyStore/index.html>
- <http://nelenkov.blogspot.co.uk/2013/08/credential-storage-enhancements-android-43.html >
- <http://www.arm.com/products/security-on-arm/trustzone>
- <https://developer.android.com/guide/topics/admin/device-admin.html>
- <https://developer.android.com/guide/topics/admin/device-admin.html#sample >
- <https://developer.android.com/work/device-management-policy.html>
- <https://developer.android.com/reference/android/content/pm/PackageManager.html#FEATURE_DEVICE_ADMIN>
