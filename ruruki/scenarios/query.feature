Feature: RUQL finding paths
    For the graph database to be useful, we need to have a way
    to extract and ask for information about the graph.

    Scenario: simple query
        Given we have a graph with vertices
            | label  | name       | surname |
            | person | Jenda      | Mudron  |
            | person | Andre      | Macedo  |
        And edges between them
            | head   | label      | tail    |
            | Jenda  | knows      | Andre   |
            | Jenda  | works_with | Andre   |
        When we query for vertices that have a name that starts with An
        Then we will get a result set with one vertice that has name Andre
        And the result returned is a result set

    Scenario: complex query
        Given we have a graph with vertices
            | label  | name       |
            | Colo   | TKO        |
            | Colo   | MAS        |
            | Host   | hostA      |
            | Host   | hostB      |
            | App    | app1       |
            | App    | app2       |
            | App    | app3       |
            | App    | app4       |
        And edges between them
            | head   | label       | tail    |
            | hostA  | belongs_to  | TKO     |
            | hostB  | belongs_to  | MAS     |
            | app1   | runs_on     | hostA   |
            | app2   | runs_on     | hostA   |
            | app3   | runs_on     | hostB   |
            | app4   | runs_on     | hostB   |
            | app3   | connects_to | app1    |
        When we query for applications that connect to TKO
        And connects to an application that belongs to MAS
        Then we will get a result set with vertex app3
