import re
from dateutil import parser
from operator import attrgetter, itemgetter
from collections import defaultdict

class EventLog:
	def __init__(self, log):
		# Example: '[1518-11-15 00:04]'
		regex = '\[(.*?)\] (.*)'
		(date,self.event) = re.findall(regex,log)[0]
		self.timestamp = parser.parse(date)

sorted_logs = sorted([EventLog(l) for l in open('input.txt','r').readlines()], key=attrgetter('timestamp'))

guard_total_sleep_time = defaultdict(int)
guard_per_minute_detail = defaultdict(lambda: defaultdict(int))
on_duty = None
fell_asleep = None

for log in sorted_logs:
	if log.event == 'falls asleep':
		fell_asleep = log.timestamp
	elif log.event == 'wakes up':
		sleep_duration = log.timestamp - fell_asleep
		guard_total_sleep_time[on_duty] += int(sleep_duration.seconds / 60)
		for minute in range(fell_asleep.minute, log.timestamp.minute):
			guard_per_minute_detail[on_duty][minute] += 1
		fell_asleep = None
	else:
		on_duty = log.event

sleepiest_guard = max(guard_total_sleep_time.items(), key=itemgetter(1))[0]
sleepiest_guard_id = int(re.findall('\d+',sleepiest_guard)[0])
sleepiest_minute = max(guard_per_minute_detail[sleepiest_guard].items(), key=itemgetter(1))[0]
sleepiest_minute_tally = guard_per_minute_detail[sleepiest_guard][sleepiest_minute]
print ('Answer 1: Guard ID #{sleepiest_guard_id} slept during minute {sleepiest_minute} {sleepiest_minute_tally} times. {sleepiest_minute}*{sleepiest_guard_id} =').format(**locals())
print (sleepiest_minute * sleepiest_guard_id)

overall_max = 0
overall_top_minute = 0
leading_guard = None
for guard in guard_per_minute_detail:
	for minute in guard_per_minute_detail[guard]:
		if guard_per_minute_detail[guard][minute] > overall_max:
			leading_guard = guard
			overall_max = guard_per_minute_detail[guard][minute]
			overall_top_minute = minute

leading_guard_id = int(re.findall('\d+',leading_guard)[0])
print ('Answer 2: Guard ID #{leading_guard_id} had the overall max minute during minute {overall_top_minute} during which he slept {overall_max} times. {overall_top_minute}*{leading_guard_id} =').format(**locals())
print (leading_guard_id * overall_top_minute)
