股票数据库系统 采用sqlite+fastapi
# sqlite3命令
```shell
sqlite> .tables
day_level      day_level_hfq
```
查看列
```shell
sqlite> PRAGMA table_info(day_level_hfq);
0|code|TEXT|0||0
1|date|TEXT|0||0
2|open|REAL|0||0
3|high|REAL|0||0
4|low|REAL|0||0
5|close|REAL|0||0
6|volume|INTEGER|0||0
```