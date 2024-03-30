# Project Design Document

## Your Project Title
--------
Prepared by:

* `<author1>`,`<organization>`
* `<author2>`,`<organization>`
* `<author3>`,`<organization>`
* `<author4>`,`<organization>`
---

**Course** : CS 3733 - Software Engineering 

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [Project Design Document](#project-design-document)
  - [Your Project Title](#your-project-title)
  - [Table of Contents](#table-of-contents)
    - [Document Revision History](#document-revision-history)
- [1. Introduction](#1-introduction)
- [2. Component-level Design](#2-component-level-design)
    - [2.1 Model](#21-model)
    - [2.2 Controller](#22-controller)
    - [2.3 View and User Interface Design](#23-view-and-user-interface-design)
- [3. References](#3-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

### Document Revision History

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2024-04-02 |Initial draft | 1.0        |
|      |      |         |         |


# 1. Introduction

Explain the purpose for providing this design document. If this is a revision of an earlier document, please make sure to summarize what changes have been made during the revision (keep this discussion brief). 


# 2. Component-level Design

(**Note**: You should describe the design for the end product (completed application) - not only your iteration1 version. You will revise this document and add more details later.)

### 2.1 Model

Provide a list of your tables (i.e., SQL Alchemy classes) in your database model and briefly explain the role of each table. 

Provide a UML diagram of your database model showing the associations and relationships among tables. 

### 2.2 Controller

Include a detailed description of the routes your application will implement. 
* Brainstorm with your team members and identify all routes you need to implement for the **completed** application.
* For each route specify its “methods”, “URL path”, and “a description of the operation it implements”.  
You can use the following table template to list your route specifications. 

|   | Methods           | URL Path   | Description  |
|:--|:------------------|:-----------|:-------------|
|1. |                   |            |              |
|2. |                   |            |              |
|3. |                   |            |              |
|4. |                   |            |              |
|5. |                   |            |              |
|6. |                   |            |              |


### 2.3 View and User Interface Design 

Explain how you plan to build the user interfaces and mention the frameworks/libraries you plan to use (e.g., Bootstrap).  

Provide a list of the page templates you plan to create and supplement your description with UI sketches or screenshots. Make sure to mention which user-stories in your “Requirements and Use Cases" document will utilize these interfaces for user interaction. 

# 3. References

Cite your references here.

For the papers you cite give the authors, the title of the article, the journal name, journal volume number, date of publication and inclusive page numbers. Giving only the URL for the journal is not appropriate.

For the websites, give the title, author (if applicable) and the website URL.

----
# Appendix: Grading Rubric
(Please remove this part in your final submission)

 * You will first  submit a draft version of this document:
    * "Project 3 : Project Design Document - draft" (5pts). 
* We will provide feedback on your document and you will revise and update it.
    * "Project 5 : Project Design Document - final" (80pts) 

Below is the grading rubric that we will use to evaluate the final version of your document. 

|**MaxPoints**| **Design** |
|:---------:|:-------------------------------------------------------------------------|
|           | Are all parts of the document in agreement with the product requirements? |
| 10        | Is the model (i.e., “database model”) explained well with sufficient detail? Do the team clearly explain the purpose of each table included in the model?| 
| 5         | Is the document making good use of semi-formal notation (i.e., UML diagrams)? Does the document provide a clear UML class diagram visualizing the DB model of the system? |
| 17        | Is the UML class diagram complete? Does it include all classes (tables) and does it clearly mark the PK and FKs for each table? Does it clearly show the associations between them? Are the multiplicities of the associations shown correctly? |
| 25        | Are all major interfaces (i.e., the routes) listed? Are the routes explained in sufficient detail? |
| 15        | Is the view and the user interfaces explained well? Did the team provide the screenshots of the interfaces they built so far.   |
|           | **Clarity** |
|           | Is the solution at a fairly consistent and appropriate level of detail? Is the solution clear enough to be turned over to an independent group for implementation and still be understood? |
| 5         | Is the document carefully written, without typos and grammatical errors?  |
| 3         | Is the document well formatted? (Make sure to check your document on GitHub. You will loose points if there are formatting issues in your document.  )  |
|           |  |
| 80         | **Total** |
|           |  |