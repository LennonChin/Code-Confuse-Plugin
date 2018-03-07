# iOS平台代码混淆脚本

> [English Description](https://github.com/LennonChin/Code-Confuse-Plugin/blob/master/README.md)

这是一款用于混淆iOS代码的插件。最近试用了几款目前很多开源的针对iOS代码混淆的插件，但混淆生成的文件一直不如人意，运行代码报错的地方依旧很多。同时有些插件实现的方式个人认为过于复杂，需要使用类似于`class-dump`的技术来进行反编译再进行混淆操作，同时很多插件使用的是直接更换需要混淆的关键字，工程过于庞大，对于代码的可读写性也有影响。于是决定自己写一个建议的插件，就有了本仓库的诞生。

## 实现原理

其实插件的实现方式十分简单，提取用户编写的文件中的方法名，使用宏定义将其更换为任意的无规则字符串。但这种方式有一些需要注意的点：

1. 对于系统库产生的方法名，不可替换；对于系统使用到的关键字，也不可以替换；否则会报错；
2. Swift混编的项目，Swift中的代码不可替换；同时Swift调用Objective-C的特定方法名也不可以轻易替换；
3. 第三方库暴露的头文件的方法名，不可替换；

根据上面的规则（可能有遗漏），该脚本采用了相对简单的方法来避免：

1. 只扫描.h和.m文件，只扫描方法名。（对于属性名，尝试过扫描，但由于属性的访问方式多样，并不建议做混淆，会产生额外的工作量）；
2. 对于系统库，让用户手动指定，这个是可以提取的，直接拿到系统库的头文件即可，脚本会自动扫描到所有的系统关键字，直接做排除处理。（以iOS11的SDK为例，系统关键字约9万个）；
3. 对于Swift代码，可以直接排除在扫描目录外；
4. 对于第三方库，用户可以手动指定目录，脚本会自动扫描提取关键字，在混淆时避免这些关键字。

依据上述原理，基本可以避免多数情况下产生的混淆错误；当然，由于各种项目的复杂性，有一些复杂的混淆错误无法避免，需要后续手动调整代码。

## 使用方式

1. clone本仓库；
2. 你需要安装python3的运行环境，这个可以使用brew进行安装，这里不再赘述。
3. 你首先需要确定以下几项：

- 提取一份你当前项目编译环境的SDK库头文件目录；（Demo中提取了iOS11的SDK头文件目录）
- 你需要混淆的代码的目录；
- 你不需要混淆的代码的目录；
- 你需要提取关键字做排除混淆的目录；（例如Pod仓库、第三方头文件）
- Swift代码目录；（理论上不会扫描替换，可以用于排除桥接文件）
- 输出文件目录；脚本运行后会产生多个log文件，以及最终需要使用到的混淆头文件；

> 注：建议目录使用绝对路径，相对路径容易出问题。

4. 确定以上几项后，找到仓库根目录的Confuse.py文件，使用以下命令行模板运行：

```shell
python3 Confuse.py \
-i 你需要混淆的代码的目录，可以是多个目录，以`,`分隔 \
-s 当前项目编译环境的SDK库头文件目录，可以是多个目录，以`,`分隔 \
-e 你不需要混淆的代码的目录，Swift代码目录，可以是多个目录，以`,`分隔 \
-c 你需要提取关键字做排除混淆的目录，可以是多个目录，以`,`分隔 \
-o 输出文件目录
```

> 注：各参数的意义如下：

- `-i`（input_dirs）：必须，项目需要处理的主要文件所在的目录
- `-s`（system_dirs）：可选，配置系统Framework文件的目录，一般用于做排除字典，避免替换系统关键字
- `-e`（exclusive_dirs）：可选，用于存放不扫描处理的文件的目录，比如Swift文件目录
- `-c`（clean_dirs）：可选，用于存放排除关键字的文件的目录，例如Pods下的目录，或者静态库（头文件修改后会出错）
- `-o`（output_dir）：必须，输出文件的目录，用于输出关键字、日志以及最后生成的混淆头文件的目录

例如我的Demo中运行脚本如下：

```shell
python3 Confuse.py \
-i /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/Confuse_Demo/Confuse_Demo/ \
-s /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/System_Frameworks_iOS11 \
-e /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/Confuse_Demo/Confuse_Demo/Swift/ \
-c /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/Confuse_Demo/Confuse_Demo/OtherSDK \
-o /Users/LennonChin/Desktop/Code-Confuse-Plugin/Demo/
```

然后回车运行即可。

> 注：在本项目中有一份示例代码，可以参考。

5. 运行后会在你指定的输出目录下产生一份Confuse.h文件，内容一般如下：

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

这份文件包含了一堆的宏定义，将需要替换的方法名都替换为了一些随机的字符串，因为宏定义是全局替换，我们只需要将该文件引入到自己的项目中，并在PCH文件中进行引入即可。

引入该文件后，Command+B测试编译，如果无法避免而产生编译错误则需要手动调整；由于将所有的替换归集到了头文件中了，所以遇到有错误的地方尝试删除对应宏定义替换信息重新编辑即可。

## License

[MIT](https://opensource.org/licenses/MIT)

Copyright (c) 2016-present, LennonChin