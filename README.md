# SecStec
## About
 - Semantically Equivalent GUI Screen detection. 
 1. input: an image pair consisting of  an error screenshot and a runtime screenshot
 2. output: a boolean telling whether the two input images are semantically same or not. 
 (whether they refer to the same error screen regardless of pixel and user data differences reside in the image pair.)
 4. widget detection: SecStec uses [UIED](https://github.com/MulongXie/UIED), an object detection tool combined old-fationed and DL models for object detection, to detect GUI element (both type and position)
 5. semantic equivalence image checker: for an image pair containing dialogue windows,using OCR technique to detect text and perform string comparison. Otherwise, 1) consturct dummy trees; 2) consturct tree shape vector and comparing vectors using cosine similarity; 3) matching indivisule tree nodes; 4) calculate tree similarity score
 
 ![SegStecv3](https://user-images.githubusercontent.com/48971920/114656895-da806680-9d29-11eb-9384-56d2a5ff8795.png)

 

## Reference
This tool related to the IEEE-SEAI paper "Image-based Bug Oracle Automation for Bug Report Reproduction Using Widget Detection" Semantically Equivalent GUI Screen detection"



