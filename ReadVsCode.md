## 选择Vscode 
```
   原因：微软的规范性以及文本编辑器的框架（如果有足够的时间 
```

## 目的
``` 
     了解迭代周期以及规范性
             计划周期内的延期任务如何安排
             对于bugfix和新功能时间预估
             模块测试规范
``` 
``` 
     了解code review的具体内容
         日常review着重检查逻辑以及性能
``` 
``` 
      近期遇到的疑惑
         临时需求如何安排？与计划冲突
         版本定义以及版本迭代的划分？bugfix推送规范？
         性能与可读性的权衡？如orm和原生sql
         计算逻辑复杂，代码逻辑风格选择
               单个函数囊括所有计算逻辑（引入模块只负责通用功能）
               类似java层层包裹封装（不易于新同学阅读代码计算，为了所谓的拓展性和兼容性，过多杂的代码）
         日志的处理，是否有接近完美的示例
```    

## 关于开发周期

### roadmap
```
   vs以6-12个月为周期制定规划
```

### 迭代周期划分
```
   以自然月迭代，每个月有单独的plan和endgame
```

### 迭代周期内

```
      week1
            减少上一次迭代遗留的债务，解决上一周期遗留的关键性债务，计划下一周期
      week2
            按week1的计划
      week3
            按week1的计划
      final week
            按测试计划测试新功能等，并补充文档
            pre-release版本，邀请用户帮忙测试
      week1
            检查监控上一周期的pre-release，并解决遗留的关键性issue
            发布pre-release
```

### Triage(任务分配>里程碑)
```
     bug和feature都会被分配到milestone里程碑，带有优先级
          严重的bug会被安排在其他bug前面
     fixbug之后确认相关issue
```

### 周期(周)盘点
```
    每周整理迭代计划，关闭已完成的feature以及分配bug修复任务；
    结束里程碑的要求，必须0bug和0issue，部分bug和feature移动到下一个里程碑
```

### 周期完结
```
    最后一个里程碑被定义为endgame，打包feature，按测试计划测试并修复严重的bug
```


### master打包
```
     确认内部版本为最新
     确认持续生成为绿色（通过状态
     如果，生成失败，从build slack channel确认通知谁处理
     如果，编译失败，push一个修复的commit病通知开发者
     如果，测试失败，提交issue给开发者修复
````

### 关于endgame分支管理

```
    1、在endgame时期创建release-1.10
    2、打包上一步的分支并系统性的测试
    3、任何严重bug都应修复并推送到master以及release-1.10，并通过步骤2
    4、无严重bug即创建tag:release-1.10.0
    5、以tag:release-1.10.0打包并推送给用户
    6、任何修复打包都应该依赖于release-1.10，补丁版本定义为：1.10.1,1.10.2...
```

### Endgame一周的安排
```
      周一：保证持续生成绿色以及冻结代码
      周二：测试
      周三：测试和fix
      周四：fix和签名认证
      周五：暂停封存任务安排表，打包master，测试、修复，更新相关issue、评论等
```

## 代码组织
```
   The core is partitioned into the following layers:
   base: Provides general utilities and user interface building blocks
   platform: Defines service injection support and the base services for Code
   editor: The "Monaco" editor is available as a separate downloadable component
   languages: For historical reasons, not all languages are implemented as extensions (yet)
         - as Code evolves we will migrate more languages to towards extensions
   workbench: Hosts the "Monaco" editor and provides the framework for "viewlets" like the Explorer, 
         Status Bar, or Menu Bar, leveraging Electron to implement the Code desktop application.
```

## 关于code review
```
https://github.com/microsoft/vscode/pulse
```
    https://github.com/microsoft/vscode/pull/82171#pullrequestreview-299623638
    实际上跟日常一样
  
### 面壁思过
```
** 理想 ** 是美好的，现实是骨感的
   1、开发周期被打乱如何抉择？
      金主需求优先，开发计划被各种打乱；
      计划基本都会按自然月，上线是没问题的，但是数据问题，如数据不全缺失等问题如何保证；
      
   2、测试规范性和客户追上线，如何抉择？
      目前缺少测试以及数据定期核查
   
   3、ccs目前大部分代码都上了ci，书写较为规范，但
         代码风格问题：面向对象的层层继承还是函数完成计算？不同同学的logic书写和逻辑划分也存在比较大的差异；
            例如save_data比较简单，可能直接写在了logic下；
               1、
                     def logic
                        get_data
                        format_data
                        algorithm
                        save_data
                     def get_data
                     def format_data
                     def algorithm
                     def save_data
               2、   
                     class logic(db, format, al, )
                        self.get_data
                        self.format_data
                        ....
                  
         易读性与性能，如何做抉择？orm和原生sql(顺带一个问题，sqlalchemy是否有接口，输出完整的查询或者插入原生sql)
         什么数据什么时候需要做检查？
         什么时候需要考虑代码的扩展性？什么时候坚决不考虑
         数据库连接需要注意什么？避免重复踩坑
            非后端框架，数据计算通常为了性能，协程多进程多线程都有使用，哪些数据库第三方包多线程安全多进程又不安全？
         对于获取数据计算问题，如果本地机器内存无法支撑取回的数据如何处理？
         
         （由于vscode上面都是大佬的代码多， 想找一些建议性的review comment有难度）
      
   5、关于jira，有两个想法
      没有一个大而全的页面，列出本周期需要fix的bug以及新功能完成状态的概览；
         按列表任务的方式过于详细，不利于大家了解全局的进展；特别是人数多了时间比较紧的项目；
      缺少了周期结束时的整理工作，未完成的工作顺利转移到下一个周期
         不需要全部人参与，全部人消耗过多时间，把控项目进展的人完成就好，例如项目经理or产品
      
   6、如何将规范执行下去？
   
```

    
