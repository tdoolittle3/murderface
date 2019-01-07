#include <iostream>
#include "ObstructionDetector.h"


 void ObstructionDetector::processFrame() {
 	auto start = cv::getCPUTickCount();
    detector >> frame;
        auto end = cv::getCPUTickCount();

        time_per_frame = (end - start) / cv::getTickFrequency();
        fps = (15 * fps + (1 / time_per_frame)) / 16;
        printf("Time per frame: %3.3f\tFPS: %3.3f\n", time_per_frame, fps);

        dst.create( frame.size(), frame.type() );
 		cvtColor( frame, frame_gray, CV_BGR2GRAY );
 }
/**
 * @function CannyThreshold
 * @brief Trackbar callback - Canny thresholds input with a ratio 1:3
 */
 void ObstructionDetector::CannyThreshold(int, void*) {
  	// Reduce noise with a kernel 3x3
 	blur( frame_gray, frameBlur, Size(3,3) );
  	// Canny detector
 	cv::Canny( frameBlur, frameBlur, lowThreshold, lowThreshold*ratio, kernel_size );
 	cv::dilate(frameBlur, frameBlur, cv::Mat(), cv::Point(-1,-1));
 	dst = cv::Scalar::all(0);
 	frame.copyTo( dst, frameBlur);
 }

cv::Mat ObstructionDetector::applyIntersectMasking(cv::Rect face) {
 	cv::Mat cmask = cv::Mat::zeros(dst.size(), CV_8UC1);
 	cv::Mat facemask = cv::Mat::zeros(dst.size(), CV_8UC1);
 	cv::rectangle(facemask, face, 255, -1, 8 ,0);

 	for (size_t i = 0; i < contours.size(); ++i) {
 		cv::rectangle(cmask, cv::boundingRect(contours[i]), 255, -1, 8 ,0);	
 	}

   	cv::Mat intersection1 = (cmask & frame_gray); // Bounding rects for contours touching face rect
 	cv::Mat intersection2 = (facemask & frame_gray); // Face bounding rect in greyscale

    intersection1 = intersection1 | intersection2;
    cv::Scalar sum1 = cv::sum(intersection1);
    cv::Scalar sum2 = cv::sum(intersection2);

    cv::Mat edgeMap;
    cvtColor(intersection1,edgeMap,CV_GRAY2RGB);

    for (size_t i = 0; i < contours.size(); ++i) {
		// approximate contour with accuracy proportional
        // to the contour perimeter            
   		cv::approxPolyDP(Mat(contours[i]), approx, arcLength(Mat(contours[i]), true)*0.02, true);
 		cv::drawContours(edgeMap, cv::Mat(approx), -1, CV_RGB(255,255,255), 1);	
   	}
    return edgeMap;
}
