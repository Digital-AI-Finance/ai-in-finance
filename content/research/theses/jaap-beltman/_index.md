---
title: "MSc Thesis Jaap Beltman | Theses at ING | AI in Finance"
description: "Developing an Early Warning System for Retail Customer Deterioration: A Data-Driven Approach"
weight: 1
draft: false
---

Beltman, J.F. (2023) Developing an Early Warning System for Retail Customer Deterioration: A Data-Driven Approach.

## Abstract

This thesis addresses the existing gap in literature concerning the prevention of retail customers from becoming overdue. The literature gap in the area of retail EWS is the lack of a comprehensive approach that incorporates multiple data sources instead of relying on a single data source, along with the need for alternative methods, such as behavioral characteristics, for identifying deteriorating clients. The purpose of this thesis is to present the design and evaluation of an EWS for retail loans. Considering that financial institutions are often subject to regulations, this thesis avoids the use of algorithms that are considered poorly interpretable. The algorithms employed in this study include logistic regression, XGBoost, and Random Forest. Additionally, a fourth model, so called meta-model, is created by using the output of the other models, as input for a new model, which is trained by a logistic regression model. Regarding overall performance, the random forest algorithm achieves an average AUC of 0.775, while XGBoost and logistic regression achieve an AUC of 0.75. The meta-model outperforms the individual models with an AUC of 0.80. Compared to the random forest model, the XGBoost and logistic regression model did fit more on their top features. The meta-model consistently achieves the best fit when using the random forest predictions, as it is the top-performing individual algorithm. XGBoost serves as the second algorithm, while the logistic regression model provides the least significant contribution to the meta-model in terms of importance. The top-performing meta-model is utilized to gain practical insights into the timeliness of the EWS signals. The model reveals that a higher threshold for warning signals results in alerts closer to the overdue date, indicating increased sensitivity to emerging client deterioration. Conversely, lower thresholds focus more on the client’s overall status. Furthermore, using the top ten features for training yields satisfactory overall results, but incorporating features beyond the top ten provides valuable supplementary information.

## Supervisors

### UT Supervisors

  * Dr. Marcos Machado
  * Dr. Jörg Osterrieder

### ING Supervisors

  * Leon Dusée
  * Dr. Markus Haverkamp

## Thesis Repository

  * [Link to thesis](https://purl.utwente.nl/essays/96525)