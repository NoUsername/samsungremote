import curses
stdscr = curses.initscr()
key = None
while key != 1:
	key = stdscr.getch()
	print "key: %s"%key