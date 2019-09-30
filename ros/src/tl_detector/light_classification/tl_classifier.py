from styx_msgs.msg import TrafficLight
import tensorflow as tf
import numpy as np
import cv2 
import rospy
import time

LIGHTS = ['Green', 'Yellow', 'Red', 'Unknown']

class TLClassifier(object):
    def __init__(self, is_site):
        if is_site:
            PATH_TO_FROZEN_GRAPH = 'light_classification/model/site_model/'
        else:
            PATH_TO_FROZEN_GRAPH = 'light_classification/model/sim_model/'
        FROZEN_GRAPH = PATH_TO_FROZEN_GRAPH + 'frozen_inference_graph.pb'
        rospy.loginfo("loading classification graph............")
        self.graph = tf.Graph()
        with self.graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(FROZEN_GRAPH, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        
            self.image_tensor = self.graph.get_tensor_by_name('image_tensor:0')
            self.detection_boxes = self.graph.get_tensor_by_name('detection_boxes:0')
            self.detection_scores = self.graph.get_tensor_by_name('detection_scores:0')
            self.detection_classes = self.graph.get_tensor_by_name('detection_classes:0')
        rospy.loginfo("loaded graph............")
        self.sess = tf.Session(graph=self.graph)

    def filter_boxes(self, min_score, boxes, scores, classes):
        """Return boxes with a confidence >= `min_score`"""
        n = len(classes)
        idxs = []
        for i in range(n):
            if scores[i] >= min_score:
                idxs.append(i)
        
        filtered_boxes = boxes[idxs, ...]
        filtered_scores = scores[idxs, ...]
        filtered_classes = classes[idxs, ...]
        return filtered_boxes, filtered_scores, filtered_classes


    def get_classification(self, image):
        """Determines the color of the traffic light in the image
        Args:
            image (cv::Mat): image containing the traffic light
        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)
        """
        image = np.dstack((image[:, :, 2], image[:, :, 1], image[:, :, 0]))
        image_np = np.expand_dims(np.asarray(image, dtype=np.uint8), 0)

        with tf.Session(graph=self.graph) as sess:                
            # Actual detection
            time0 = time.time()
            (boxes, scores, classes) = sess.run([self.detection_boxes, self.detection_scores, self.detection_classes], 
                                                feed_dict={self.image_tensor: image_np})

            time1 = time.time()
            print("Prediction time in milliseconds", (time1 - time0) * 1000)

            # Remove unnecessary dimensions
            boxes = np.squeeze(boxes)
            scores = np.squeeze(scores)
            classes = np.squeeze(classes)
        
            confidence_cutoff = 0.7
            # Filter boxes with a confidence score less than `confidence_cutoff`
            boxes, scores, classes = self.filter_boxes(confidence_cutoff, boxes, scores, classes)
        
        
        if len(classes)>0:
            color_state = int(classes[np.argmax(scores)])
            
            if color_state == 1:
		 rospy.loginfo("traffic light color from classification is GREEN")	
                 return TrafficLight.GREEN
            elif color_state == 2:
		 rospy.loginfo("traffic light color from classification is RED")
                 return TrafficLight.RED
            elif color_state == 3:
		 rospy.loginfo("traffic light color from classification is YELLOW")
                 return TrafficLight.YELLOW
        rospy.loginfo("traffic light color from classification is UNKNOWN")                    
        return TrafficLight.UNKNOWN

