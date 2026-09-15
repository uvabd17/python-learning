"""
LESSON 1b - the same six ideas, no answers given
================================================

You finished 02_python_you_need.py, but the hints in that file were the answers,
so there was nothing left to work out. This time you get the GOAL and the NAME of
the tool. Not the code.

RULES
  1. Close 02_python_you_need.py. Do not look at it.
  2. Get it wrong. Run the file, read what it says, try again.
  3. If you are stuck for more than five minutes on one, send it to me.

    python3 ~/journey_to_ML/python-learning/ai-engineering/03_do_it_again.py
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = "/home/yuvaraj-ambati/HCP/hcp/data/posts/all_posts.json"
DATA = FULL if os.path.exists(FULL) else os.path.join(HERE, "data", "hydtp_sample.json")

posts = json.load(open(DATA, encoding="utf-8"))["posts"]

# A reminder of what one post looks like, since you will need the key names:
#
#   {"id": "...", "platform": "twitter", "date": "2026-04-10",
#    "day_of_week": "Friday", "time_slot": "afternoon", "format": "image",
#    "text": "...", "language": "english", "hashtag_count": 2,
#    "mention_count": 0, "has_cta": false,
#    "tags": {"topics": [...], ...}}


# ─────────────────────────────────────────────────────────────────
# 1. The LAST post in the list.
#    Tool: square brackets. Negative numbers count from the end.
# ─────────────────────────────────────────────────────────────────
last_post = posts[-1]


# ─────────────────────────────────────────────────────────────────
# 2. The day of the week that last post went out on.
#    Tool: dict access on the answer to 1.
# ─────────────────────────────────────────────────────────────────
last_day = last_post["day_of_week"]


# ─────────────────────────────────────────────────────────────────
# 3. How many posts have a call to action?
#    The key is "has_cta" and its value is already True or False.
#    Tool: a loop, an if, and a counter.
#    (There is a shorter way using sum(). Do it the long way first.)
# ─────────────────────────────────────────────────────────────────
count=0
for post in posts:
    if post["has_cta"]:
        count+=1
cta_count = count


# ─────────────────────────────────────────────────────────────────
# 4. How many posts went out on each day of the week?
#    You want something like {"Monday": 240, "Tuesday": 198, ...}
#    Tool: an empty dict, a loop, and the same counting pattern as 3
#          except the counter lives inside the dict.
#
#    This is the one that matters most. Counting into a dict IS how you
#    score an eval set later.
# ─────────────────────────────────────────────────────────────────
day_count={}
for post in posts:
    day=post["day_of_week"]
    if day not in day_count:
        day_count[day]=0
    day_count[day]=day_count[day]+1

day_counts = day_count


# ─────────────────────────────────────────────────────────────────
# 5. Every post that uses more than 3 hashtags.
#    A LIST of the posts themselves, not a count.
#    Tool: an empty list, a loop, an if, and .append()
# ─────────────────────────────────────────────────────────────────
hashtag=[]
for post in posts:
    if post["hashtag_count"]>3:
        hashtag.append(post)
hashtag_heavy = hashtag


# ─────────────────────────────────────────────────────────────────
# 6. Write a function that takes one post and returns HOW MANY topics
#    it was tagged with. Some posts have no tags at all, so it must
#    return 0 for those instead of crashing.
#
#    Topics live at post["tags"]["topics"], which is a list.
#    Tool: def, .get() so a missing key gives you None instead of an error,
#          len() for the count.
# ─────────────────────────────────────────────────────────────────
def topic_count(post):
    topic=post.get("tags")
    if topic is not None:
        if topic["topics"] is not None:
            return len(topic["topics"])
    return 0
print(topic_count({"id": "x", "text": "a post with no tags at all"}))
# ─────────────────────────────────────────────────────────────────
# 7. Use your own function. What is the highest number of topics any
#    single post was given?
#    Tool: a loop, topic_count(post), and keeping track of the biggest
#          number you have seen so far.
# ─────────────────────────────────────────────────────────────────
top_cnt=0
for post in posts:
    top_cnt=max(top_cnt, topic_count(post))
most_topics = top_cnt


# ═════════════════════════════════════════════════════════════════
#  Checker. Don't edit below here.
# ═════════════════════════════════════════════════════════════════

def check(n, what, got, ok, nudge):
    if got is None:
        print(f"  [ ] {n}. {what:<18} not attempted")
    elif ok:
        print(f"  [x] {n}. {what:<18} correct   {str(got)[:46]}")
    else:
        print(f"  [!] {n}. {what:<18} not yet")
        print(f"         you have: {str(got)[:58]}")
        print(f"         {nudge}")

want_day_counts = {}
for _p in posts:
    want_day_counts[_p["day_of_week"]] = want_day_counts.get(_p["day_of_week"], 0) + 1
want_heavy = [p for p in posts if p.get("hashtag_count", 0) > 3]
def _want_tc(p):
    t = p.get("tags")
    return len(t.get("topics", [])) if t else 0

print("\n" + "=" * 66)
print("  LESSON 1b - do it again, from memory")
print("=" * 66 + "\n")

check(1, "last_post", last_post, last_post is posts[-1],
      "a list index can be negative")
check(2, "last_day", last_day, last_day == posts[-1]["day_of_week"],
      "reach into the post you found in 1")
check(3, "cta_count", cta_count, cta_count == sum(1 for p in posts if p.get("has_cta")),
      "start a counter at 0 before the loop, not inside it")
check(4, "day_counts", day_counts, day_counts == want_day_counts,
      "seven keys, and the values must add up to " + str(len(posts)))
check(5, "hashtag_heavy", hashtag_heavy,
      isinstance(hashtag_heavy, list) and len(hashtag_heavy) == len(want_heavy),
      "append the whole post, not the count. Expected " + str(len(want_heavy)) + " of them")
try:
    r6 = topic_count(posts[0])
    ok6 = r6 == _want_tc(posts[0])
except Exception as e:
    r6, ok6 = "crashed: " + str(e), False
check(6, "topic_count()", r6, ok6, "return 0 when there are no tags, never None")
check(7, "most_topics", most_topics, most_topics == max(_want_tc(p) for p in posts),
      "keep a 'biggest so far' variable and replace it when you beat it")

done = sum([
    last_post is posts[-1],
    last_day == posts[-1]["day_of_week"],
    cta_count == sum(1 for p in posts if p.get("has_cta")),
    day_counts == want_day_counts,
    isinstance(hashtag_heavy, list) and len(hashtag_heavy) == len(want_heavy),
    ok6,
    most_topics == max(_want_tc(p) for p in posts),
])
print(f"\n  {done} of 7.")
if done == 7:
    print("  Now close this file and tell me what exercise 4 does, in your own words.\n")
else:
    print()
