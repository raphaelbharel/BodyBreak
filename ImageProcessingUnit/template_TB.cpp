//INSTRUCTIONS FOR USE ON PC
//1. Change absolute paths to your own image folder
//2. Make sure int w = width of image in question, same for h = _
// default for 1080p is 1920x1080 pixels.

#include <ap_fixed.h>
#include <ap_int.h>
#include <cassert>
#include <iostream>

#include <hls_opencv.h>

typedef ap_uint<8> pixel_type;
typedef ap_int<8> pixel_type_s;
typedef ap_uint<96> u96b;
typedef ap_uint<32> word_32;
typedef ap_ufixed<8,0, AP_RND, AP_SAT> comp_type;
typedef ap_fixed<10,2, AP_RND, AP_SAT> coeff_type;

struct pixel_data {
	pixel_type blue;
	pixel_type green;
	pixel_type red;
};


void template_filter(volatile uint32_t* in_data, volatile uint32_t* out_data, int w, int h, int parameter_1);
int distance(int refx, int refy, int px, int py);
void mapping_function(volatile uint32_t* in_data, volatile uint32_t* out_data, int w, int h, int parameter_1, int d);

int main() {

	//Specify Input Image Absolute Path
	cv::Mat src_hls = cv::imread("/home/dyl17/test_map/bg1.jpg", CV_LOAD_IMAGE_UNCHANGED);
	std::cout << "Image type: " << src_hls.type() << ", no. of channels: " << src_hls.channels() << std::endl;


	std::cout<<"SIZE  "<<src_hls.size()<<std::endl;
	uchar *data_p = src_hls.data;

	//Make sure that these much input image resolution
	int w = 1920;
	int h = 1080;

	int parameter_1 = 0; //currently unused

	uchar *image = (uchar *)malloc(w*h*4);

	for (int i=0; i<w*h; i++){
		image[4*i + 0] = data_p[3*i + 2]; //R - R
		image[4*i + 1] = data_p[3*i + 1]; // B - B
		image[4*i + 2] = data_p[3*i + 0]; // G - G
		image[4*i + 3] = 0;
	}

	 template_filter((volatile uint32_t *)image, (volatile uint32_t *)image, w, h, parameter_1);

	for (int i=0; i<w*h; i++){
		data_p[3*i + 2] = image[4*i + 0];
		data_p[3*i + 1] = image[4*i + 1];
		data_p[3*i + 0] = image[4*i + 2];
	}

	//Specify an Absolute Path for Storing Output Image
	cv::imwrite("/home/dyl17/test_map/out.jpg",src_hls);

	free(image);

	return 0;

}
