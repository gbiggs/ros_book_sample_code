#!/usr/bin/env python

import rospy

from chapter4.srv import WordCount, WordCountResponse


def count_words(request):
    return WordCountResponse(len(request.words.split()))
    # or:
    # return len(request.words.split())
    # or:
    # return [len(request.words.split())]
    # or:
    # return {'count': len(request.words.split())}


rospy.init_node('service_server')

service = rospy.Service('word_count', WordCount, count_words)

rospy.spin()
