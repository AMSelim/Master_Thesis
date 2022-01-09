from typing import List
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.neighbors import KNeighborsClassifier


def write_results(true_labels, predicted_labels, results_file_path):
    accuracy = accuracy_score(y_true=true_labels, y_pred=predicted_labels)
    # Instead of micro
    # Should be macro
    precision, recall, fscore, support = precision_recall_fscore_support(y_true=true_labels, y_pred=predicted_labels,
                                                                         average='micro', zero_division=0)
    with open(results_file_path, "a") as text_file:
        text_file.write(f"{accuracy}\t{precision}\t{recall}\t{fscore}\n")


def classify_data(training_data_list: List[np.ndarray], training_labels_list: List[int],
                  testing_data_list: List[np.ndarray], testing_labels_list: List[int], results_file_path: str):
    classifier_1 = SVC(gamma="auto", kernel="rbf", probability=True, random_state=0)
    classifier_2 = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
    classifier_3 = RandomForestClassifier(random_state=0)
    classifier_4 = RandomForestClassifier(random_state=0, n_estimators=450)
    classifier_5 = RandomForestClassifier(random_state=0, criterion="entropy")
    classifier_6 = RandomForestClassifier(random_state=0, n_estimators=50)
    classifier_7 = RandomForestClassifier(random_state=0, n_estimators=300)
    classifier_8 = KNeighborsClassifier(n_neighbors=7)
    for clf in [classifier_1, classifier_2, classifier_3, classifier_4, classifier_5, classifier_6, classifier_7,
                classifier_8]:
        clf.fit(X=training_data_list, y=training_labels_list)
        predicted_labels = clf.predict(testing_data_list)
        write_results(true_labels=testing_labels_list, predicted_labels=predicted_labels,
                      results_file_path=results_file_path)
    print("Classification Done")
    with open(results_file_path, "a") as text_file:
        text_file.write("\n")
