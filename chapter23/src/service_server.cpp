#include <ros/ros.h>
#include <chapter23/WordCount.h>

#include <string>

bool count(chapter23::WordCount::Request &req,
           chapter23::WordCount::Response &res) {
  std::string::size_type l = req.words.length();
  int count(0);
  if (l == 0)
    count = 0;
  else {
    count = 1;
    for(int i = 0; i < l; ++i)
      if (req.words[i] == ' ')
        ++count;
  }
  res.count = count;
  return true;
}


int main(int argc, char **argv) {
  ros::init(argc, argv, "count_server");
  ros::NodeHandle node;

  ros::ServiceServer service = node.advertiseService("count", count);

  ros::spin();

  return 0;
}
