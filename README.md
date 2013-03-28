pcp - Parallel Copy

When single threads just aren't enough!



Single level copying 20 files

$ du -h ~/cptest/from/
9.8G /home/ecko/cptest/from/

$ time cp -r ~/cptest/from/ ~/cptest/to

real    0m32.204s
user    0m0.193s
sys 0m23.680s

$ time python pcp.py ~/cptest/from/ ~/cptest/to/

real    0m17.802s
user    0m5.408s
sys 0m42.321s


Multi level copying 20 files in each dir

$ du -h ~/cptest/from/
1.2G    /home/ecko/cptest/from/level_one/level_two
3.2G    /home/ecko/cptest/from/level_one
13G /home/ecko/cptest/from/

$ time cp -r ~/cptest/from/* ~/cptest/to/

real    0m33.760s
user    0m0.274s
sys 0m30.149s

$ time python pcp.py ~/cptest/from/ ~/cptest/to/

real    0m24.000s
user    0m4.449s
sys 0m43.357s


Multi level  copying 100 files in each dir 20G each

$ du -h ./from/
2.0G    ./from/level_one/level_two/level_three
4.0G    ./from/level_one/level_two
5.9G    ./from/level_one
2.0G    ./from/level_one_a
9.8G    ./from/

$ time cp -r ~/cptest/from/* ~/cptest/to/

real    0m21.992s
user    0m0.218s
sys 0m21.244s

$ time python pcp.py ~/cptest/from/ ~/cptest/to/

real    0m12.946s
user    0m4.235s
sys 0m38.593s

