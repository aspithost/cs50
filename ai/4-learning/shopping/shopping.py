import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    NUMERIC_TYPES = {
        "int": [0, 2, 4, 11, 12, 13, 14],
        "float": [1, 3, 5, 6, 7, 8, 9]
    }

    MONTHS = {
        "feb": 1,
        "mar": 2,
        "may": 4,
        "june": 5,
        "jul": 6,
        "aug": 7,
        "sep": 8,
        "oct": 9,
        "nov": 10,
        "dec": 11
    }

    evidence = []
    labels = []

    with open(filename, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        # Skip first line of headers
        next(reader)
        for row in reader:
            # Assign value for label
            label = row.pop()
            labels.append(1 if label.lower() == "true" else 0)

            # Format evidence to correct values
            for (index, value) in enumerate(row):
                # format month
                if index == 10:
                    row[index] = MONTHS[value.lower()]
                # Format visitor type
                elif index == 15:
                    row[index] = 1 if value.lower() == "returning_visitor" else 0
                # Format weekend
                elif index == 16:
                    row[index] = 1 if value.lower() == "true" else 0
                elif index in NUMERIC_TYPES["int"]:
                    row[index] = int(value)
                elif index in NUMERIC_TYPES["float"]:
                    row[index] = float(value)
            evidence.append(row)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(evidence, labels)
    return knn


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_correct = 0
    true_incorrect = 0
    false_correct = 0
    false_incorrect = 0
    for label, prediction in zip(labels, predictions):
        if label == 0:
            if prediction == 0:
                false_correct += 1
                continue
            false_incorrect += 1
            continue
        if prediction == 1:
            true_correct += 1
            continue
        true_incorrect += 1

    sensitivity = true_correct / (true_correct + true_incorrect) if (true_correct + true_incorrect) != 0 else 0
    specificity = false_correct / (false_correct + false_incorrect) if (false_correct + false_incorrect) != 0 else 0

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
