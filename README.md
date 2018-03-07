# iOS platform code confusion script

> [中文版说明](https://github.com/LennonChin/Code-Confuse-Plugin/blob/master/README_zh-cn.md)

This is a plug-in for obfuscating iOS code. Recently tried several open source plug-in currently for iOS code confusion, but the confusion generated files are unsatisfactory, the code is still having a lot of errors when running in some places. At the same time, the way some plug-ins to achieve it is too complicated in my personally think, you need to use something similar to `class-dump` technology to decompile and then obfuscate the operation, while many plug-ins are replace the keywords which need to confuse directly, this work is too large and the code Readability is also affected. So I decided to write a suggestion plug-in, there is the birth of this warehouse.

## Realize the principle

In fact, the implementation of the plug-in is very simple, extract the user-written file name in the method, use the macro definition to replace it with any random string. But this way there are some points to note:

1. for the system library generated method name, can not be replaced; for the system to use the keyword, can not be replaced; otherwise it will error;
2. Swift hybrid project, the code in Swift can not be replaced; at the same time Swift called Objective-C specific method name can not be easily replaced;
3. The third party library exposed header file name, can not be replaced;

Based on the above rules (which may be missing), the script takes a relatively simple approach to avoid:

1. Only scan the .h and .m files, only scan the method name. (For attribute names, I've tried scanning, but due to the variety of attribute access, I do not recommend obfuscation and extra work)
2. For the system library, let the user manually specify, this can be extracted directly to the system library header files, the script will automatically scan all the system keywords, do the exclusion. (To iOS11 SDK for example, the system key about 90,000);
3. Swift code can be directly excluded from the scan directory;
4. For third-party libraries, users can manually specify directories, scripts automatically scan for extracted keywords, and avoid them when confused.

Based on the above principle, the obfuscation error generated in most cases can be basically avoided; of course, due to the complexity of various projects, some complicated obfuscation errors can not be avoided and the subsequent manual adjustment of the code is needed.

## How to use

1. Clone this repository
2. You need to install python3 operating environment, this can be used to install brew, not repeat them here.
3. You first need to determine the following:

- Extract a directory of SDK library files for your current project compilation environment (extract the SDK header files for iOS11 in Demo)
- you need to confuse the directory of code;
- You do not need to confuse the directory of code;
- You need to extract keywords to exclude obfuscated directories; (eg Pod repository, third party headers)
- Swift code directory; (theoretically not scan replace, can be used to exclude bridging files)
- Output file directory; After running the script will produce multiple log files, as well as the final need to use the confusion header file;

4. After confirming the above items, locate the Confuse.py file in the root directory of the repository and run it with the following command line template:

```shell
python3 Confuse.py \
-i You need to confuse the directory of the code, which can be multiple directories, separated by `,`
-s The SDK project library directory for the current project's build environment, which can be multiple directories separated by `,`
-e You do not need to confuse the directory of code, Swift code directory, can be more than one directory, separated by `,` \
-c You need to extract keywords to exclude obfuscated directories, which can be multiple directories separated by `,`
-o output file directory
```

> Note: The meaning of each parameter is as follows:

- `-i` (input_dirs): must, the project needs to deal with the main file directory
- `-s` (system_dirs): Optional, configure the system framework file directory, generally used to exclude dictionary, to avoid replacing the system keyword
- `-e` (exclusive_dirs): Optional, a directory for storing files that are not scanned, such as the Swift file directory
- `-c` (clean_dirs): Optionally, a directory for files that exclude keywords, such as directories under Pods, or static libraries (error after header file modification)
- `-o` (output_dir): Required, output file directory, directory for output of keywords, logs, and finally generated obfuscated header files

For example, my Demo running script is as follows:

```shell
python3 Confuse.py \
-i /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/Confuse_Demo/Confuse_Demo/ \
-s /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/System_Frameworks_iOS11 \
-e /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/Confuse_Demo/Confuse_Demo/Swift/ \
-c /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/Confuse_Demo/Confuse_Demo/OtherSDK \
-o /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/
```

Then press Enter to run.

> Note: In this project there is a sample code, you can refer to.

5. After the operation will produce a Confuse.h file in your specified output directory, the content is generally as follows:

```c
#define NEED_CONFUSE 1
#if NEED_CONFUSE
// create time at 2018-03-07 11:08:29.482661
#define thisIsATestFunctionWithoutParameters EHIFIFFCDEDBDAEHAHJECHHDJABBEFIE
#define thisIsATestFunctionWithParameter1 FGCCAACHEFDEDEABBEDHDAACEEEFFDDB
#define thisIsAPublicFunctionWithParameter1 BCCAFCBBAAACDACBJAJJGEJHDCAHIFAJ
#define thisIsAPublicFunctionWithoutParameters FBIBCDBBEDJADFIBBBFJIJACCFJIAACE
#endif
```

This file contains a bunch of macro definitions that replace the name of the method that needs to be replaced with some random string because the macro definition is a global replacement and we just need to bring the file into your own project and in the PCH file In the introduction can be.

After the introduction of the document, the Command + B test compilation, if you can not avoid the compilation error, you need to manually adjust; due to all the replacement will be collected into the header file, so in the wrong place to try to delete the corresponding macro definition replacement information Re-editing can be.

## License

[MIT](https://opensource.org/licenses/MIT)

Copyright (c) 2016-present, LennonChin
