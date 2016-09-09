#include <ros/ros.h>
#include <chapter23/WordCount.h>

#include <iostream>


int main(int argc, char **argv) {
  ros::init(argc, argv, "count_client");
  ros::NodeHandle node;

  ros::ServiceClient client = node.serviceClient<chapter23::WordCount>("count");

  chapter23::WordCount srv;
  srv.request.words = "one two three four";

  if (client.call(srv))
    std::cerr << "success: " << srv.response.count << std::endl;
  else
    std::cerr << "failure" << std::endl;
  return 0;
}
