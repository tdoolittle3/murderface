#pragma once

#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include "VideoFaceDetector.h"


class ObstructionDetector
{
public:
	ObstructionDetector();
	~ObstructionDetector();

	VideoFaceDetector detector;
 Mat frame, frame_gray;
 Mat dst, frameBlur;
 vector<Point> approx;
 int edgeThresh = 1;
 int lowThreshold = 20;
 int const max_lowThreshold = 100;
 int ratio = 3;
 int kernel_size = 3;
 std::vector<std::vector<cv::Point> > contours;

 const cv::String	WINDOW_NAME("Microphone Detector");
 const cv::String	CASCADE_FILE("haarcascade_frontalface_default.xml");

}