#include <ap_fixed.h>
#include <ap_int.h>
#include <stdint.h>
#include <assert.h>
#include <vector>

typedef ap_uint<8> pixel_type;
typedef ap_int<8> pixel_type_s;
typedef ap_uint<96> u96b;
typedef ap_uint<32> word_32;
typedef ap_ufixed<8,0, AP_RND, AP_SAT> comp_type;
typedef ap_fixed<10,2, AP_RND, AP_SAT> coeff_type;

double rgb [5][3] =  { {0.482, 0.225, 0.293}, // PINK //, //{225, 225, 95}, // yellow
					   {0.508, 0.3153, 0.1756},// orange  //green
					   {0.42, 0.44, 0.16}, //yellow
					   {200, 200, 200}, //orange
					   {200, 200, 200}  // blue
};


struct pixel_data {
    pixel_type blue;
    pixel_type green;
    pixel_type red;
};

int distance(int refx, int refy, int px, int py);
int reference [4] = {300, 300};

void template_filter(volatile uint32_t* in_data, volatile uint32_t* out_data, int w, int h, int parameter_1){
#pragma HLS INTERFACE s_axilite port=return
#pragma HLS INTERFACE s_axilite port=parameter_1
#pragma HLS INTERFACE s_axilite port=w
#pragma HLS INTERFACE s_axilite port=h

#pragma HLS INTERFACE m_axi depth=2073600 port=in_data offset=slave // This will NOT work for resolutions higher than 1080p
#pragma HLS INTERFACE m_axi depth=2073600 port=out_data offset=slave

int countpink = 0;
int countorange = 0;

int avxpink = 0;
int avypink = 0;

int avxorange = 0;
int avyorange = 0;

    for (int i = 0; i < h; i++) {

        int last_gray = 0;

        for (int j = 0; j < w; j++) {

#pragma HLS PIPELINE II=1
#pragma HLS LOOP_FLATTEN off

            unsigned int current = *in_data++;

            double precision = 0.075;
            unsigned char in_r = current & 0xFF;
            unsigned char in_g = (current >> 8) & 0xFF;
            unsigned char in_b = (current >> 16) & 0xFF;

            unsigned char out_r = 0;
            unsigned char out_b = 0;
            unsigned char out_g = 0;

            unsigned char in_t = in_r + in_g + in_b;
            int in_red = in_r;
            int in_green = in_g;
            int in_blue = in_b;
            int in_total =  in_red + in_green + in_blue;// in_red + in_green + in_blue;
            int test_red = 0.9*rgb[0][0]*in_t;

            if ((in_r > (1-precision)*rgb[0][0]*in_total &&
            	 in_r < (1+precision)*rgb[0][0]*in_total) &&
            	(in_g > (1-precision)*rgb[0][1]*in_total &&
            	 in_g < (1+precision)*rgb[0][1]*in_total) &&
				(in_b > (1-precision)*rgb[0][2]*in_total &&
				 in_b < (1+precision)*rgb[0][2]*in_total)){

                  out_r = 0xFF;
                  out_g = 0x00;
                  out_b = 0x00;

                  avxpink += j;
                  avypink += i;
                  countpink++;

            } else if ((in_r > (1-precision)*rgb[2][0]*in_total &&
            			in_r < (1+precision)*rgb[2][0]*in_total) &&
            		   (in_g > (1-precision)*rgb[2][1]*in_total &&
            		    in_g < (1+precision)*rgb[2][1]*in_total) &&
					   (in_b > (1-precision)*rgb[2][2]*in_total &&
					    in_b < (1+precision)*rgb[2][2]*in_total)){

            	out_r = 0x00;
                out_g = 0xFF;
                out_b = 0x00;
                avxorange += j;
                avyorange += i;
                countorange++;


            } else{
                out_r = in_r;
                out_g = in_g;
                out_b = in_b;
            }

            unsigned int output = out_r | (out_g << 8) | (out_b << 16);
            *out_data++ = output;

        }

    }
    avxpink = avxpink/countpink;
    avypink = avypink/countpink;
    avxorange = avxorange/countorange;
    avyorange = avyorange/countorange;
    std::cout << "average pink x is " << avxpink << std::endl;
    std::cout << "average pink y is " << avypink << std::endl;
    std::cout << "average orange x is " << avxorange << std::endl;
    std::cout << "average orange y is " << avyorange << std::endl;
    std::cout << "distance between pink and orange " << distance(avxpink, avypink, avxorange, avyorange) << std::endl;
}

void mapping_function(volatile uint32_t* in_data, volatile uint32_t* out_data, int w, int h, int parameter_1, int d){
	// Ports
	#pragma HLS INTERFACE s_axilite port=return
	#pragma HLS INTERFACE s_axilite port=parameter_1
	#pragma HLS INTERFACE s_axilite port=w
	#pragma HLS INTERFACE s_axilite port=h

	#pragma HLS INTERFACE m_axi depth=2073600 port=in_data offset=slave // This will NOT work for resolutions higher than 1080p
	#pragma HLS INTERFACE m_axi depth=2073600 port=out_data offset=slave
	// Init
	double threshold = 0.1*w;
	// Map distance to intensity
	double intensity = 0;
	if (d > threshold) {
		intensity = 0;
	} else if (d <= 0) {
		intensity = 1;
	} else {
		// Linear relationship between intensity and d
		intensity = 1-(d/threshold);
	}
	std::cout << "d = " << d << std::endl;
	std::cout << "threshold = " << threshold << std::endl;
	std::cout << "I = " << intensity << std::endl;

	double rgb_transform = 1-intensity;

	std::cout << "RGB transform = " << rgb_transform << std::endl;

	// Display heatmap (whole screen)

	for (int i = 0; i < h*w; ++i) {

	#pragma HLS PIPELINE II=1
	#pragma HLS LOOP_FLATTEN off

					unsigned int current = *in_data++;
					unsigned char in_g = (current >> 8) & 0xFF;
					unsigned char in_b = (current >> 16) & 0xFF;
					unsigned char out_g = in_g*rgb_transform;
					unsigned char out_b = in_b*rgb_transform;

					unsigned int output = (current & 0xFF) | (out_g << 8) | (out_b << 16);
					*out_data++ = output;

	}
}


int distance(int refx, int refy, int px, int py){ // use custom precision
	return sqrt((refx-px)*(refx-px)+(refy-py)*(refy-py));
}
