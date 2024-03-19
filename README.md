# Test with Nao
- Connect to the same network as Nao. (The black router in Insyghtlab) 
- Test if the Nao is connected correctly by accessing it through the browser. The id/password is nao/nao.
- Make sure the `IP` in `main.py` is correct
- Make sure `ROBOT_EXIST = True` in `main.py`

# Test without Nao
- Make sure `ROBOT_EXIST = False` in `main.py`

# Run the program
1. install required pkg: https://socialrobotics.atlassian.net/wiki/spaces/CBSR/pages/2180415493/Install
2. run `redis-server conf/redis/redis.conf` in the `framework` folder
3. run `main.py`

# Trouble shoot
When running Reddis, if
```
Failed listening on port XXXX (tcp), aborting
```
Find the process id by `ps aux | grep redis` and kill the process with `kill -9 $pid`