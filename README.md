# sit-stand
*created intially by Kenneth Lai. ~May 2017*

*Please feel free to send any questions to: hykenneth.lai@berkeley.edu*

## File Descriptions
- **adaptive*.py**: Algorithms for step count
- **dataReader.py**: reads all data (sit, stand, walk) into dataFrames. The data files (.csv) are located in the data folder.
- **realTimePred.py**: functions for running real-time prediction
- **realTimePredMain.py**: run this file to test real-time prediction with the sensor.
- **stepCountMain.py**: takes in a dataFrame (walking) and does step count.
- **utils.py**: Lots of functions dealing with formatting data, creating test verification datasets, moving intervals, etc.
- **verification.py**: verification on several different motion protocols (for exmaple: switching for stand to sit). Also includes `testHyperParam`, the function that optimizes for threshold and interval.
- **verificationContinuous.py**: similar to above but uses a moving average dataset for testing
- **verificationNew.py**: functions for testing (w/o protocols). Produces confusion matrix and classification reports. Use `testHyperParam` to find the best threshold and interval to use in `accuracyTest`

## To Run Verification
1. With designed protocols:
    1. See top of `verification.py` to see how to design protocols
    2. create Target with the function `createPattern`, located in `verification.py`
    3. run `testHyperParam`. `datasets` should be your recorded data for that specific protocol. `patterns` is the target that you created in the previous step. This step can be skipped. 
    3. use `testMotion`, with your recorded dataset, target, interval, and threshold. 
2. Without protocols (just verifying accuracy of raw data):
    1. Run `accuracyTest` located in **verificationNew.py**. This should take all data that is processed in **dataReader.py**.


