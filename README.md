# bondfuture_trade_history

根据文华或者快期导出来的交易记录，生成15Min bar对应的买卖点。

使用时，修改main.py中的data_folder_path参数和target_file参数，然后运行即可。

文华导出的时候会带上交易日期，故而处理相对简单一些，但是文华的软件在交易时间段之后会自动退出，导致无法导出成交记录。

快期导出的文件不带交易日期，且导出文件的命名为操作日期，故而需要进行交易日期的推断。

规则如下：如果当日为交易日，且文件修改时间小于当日21点，则认为是当日的交易，使用文件名中的日期作为交易日；
如果当时为非交易日，则交易日期应为下一个交易日；
如果当日为交易日，但是文件修改时间大于21点，则表示当前导出的记录为当日的夜盘，则应该归属于下一个交易日；


对于当日多次导出的处理：文华会在原有文件的基础上进行append，故而无需担心交易被覆盖的问题，在生成记录时去重即可；快期导出时会将文件覆盖，故而需要小心夜盘覆盖日盘的数据。如果在导出之后运行程序，则会根据文件修改时间自动进行备份，即如果文件修改时间小于21点，则备份文件，且会覆盖之前的备份，如果大于等于21点，则不进行文件备份。