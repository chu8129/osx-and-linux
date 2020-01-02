## 关于MySQL跨网的性能问题(同子网区别不大)

```
背景：CCS项目
    CCS线上环境在阿里云，物理机(性能机器)在独立的子网，计算结果需要同步到线上mysql
	项目：sqlalchemy，autoflush=True, autocommit=False
```
```
测试：
	shell: 生成sql文件秒级别完成；
	项目：10minute+
```
```
修改：
	autoflush:false
```
```
检查性能问题神器：
	SET GLOBAL log_output = "FILE"; the default.
	SET GLOBAL general_log_file = "/path/to/your/mysql.log";
	SET GLOBAL general_log = 'ON';
```
```
理解：
	flush 预提交，等于提交到数据库内存，还未写入数据库文件
	commit 就是把内存里面的东西直接写入，可以提供查询了
	
	session.commit() 
		将数据库内存中的数据提交到数据库，内部调用session.flush()，其余的事务可以访问最新的数据；
	session.rollback() 
		是回滚当前事务的变更数据操作；
	session.flush() 
		在事务管理内与数据库发生交互, 对应的实例状态被反映到数据库，
		比如自增 ID，但是数据库中当前事务的数据值并未更新上；
		相当于预提交，等于提交到数据库内存，还未写入数据库文件；
		deletions and modifications to the database as INSERTs, DELETEs, UPDATE；
	
	
```
```
原因：
	假设你每秒的网络延迟是0.01ms，不算数据处理时间
	如果是autoflush=true，那么10w次时间：100000 * 0.01=1000s～=16.6minute
	autoflush的问题就在这了，对于小数据影响不大，比如索引查询

```
```
重现：
	...
```


## 关于merge问题
```
    primarykey字段：尽量有唯一的主键，并且是可预知的
	原因：django需要，sqlalchemy的merge也需要用来判断
```
