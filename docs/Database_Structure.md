# Rough Outline

```sql
CREATE TABLE User (
    id UUID PRIMARY KEY NOT NULL,
    username varchar(50),
    password varchar(50),
    /* etc... */
);

CREATE TABLE Budget (
    budget_id UUID PRIMARY KEY NOT NULL,
    budget_name varchar(50),
    user_id UUID NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE Account (
    account_id UUID PRIMARY KEY NOT NULL,
    account_name varchar(50),
    account_type varchar(50),
    balance float,
    cleared_balance float,
    uncleared_balance float,
    working_balance float,
);

CREATE TABLE Account_Budget (
    account_id UUID NOT NULL,
    budget_id UUID NOT NULL,
    PRIMARY KEY (account_id, budget_id),
    FOREIGN KEY (account_id) REFERENCES Account(account_id),
    FOREIGN KEY (budget_id) REFERENCES Budget(budget_id)
);

CREATE TABLE Payee (
    payee_id UUID PRIMARY KEY NOT NULL,
    payee_name varchar(50)
);

CREATE TABLE Category_Group (
    category_group_id UUID PRIMARY NOT NULL,
    category_group_name varchar(50),
);

CREATE TABLE Category (
    category_id UUID PRIMARY NOT NULL,
    category_name varchar(50),
    target_type varchar(50),
    amount float,
    budget_id UUID NOT NULL,
    category_group_id UUID,
    FOREIGN KEY (category_group_id) REFERENCES Category_Group(category_group_id),
    FOREIGN KEY (budget_id) REFERENCES Budget(budget_id)
);

CREATE TABLE Transactions (
    transaction_id UUID PRIMARY KEY NOT NULL,
    inflow int,
    outflow int,
    date date,
    cleared boolean,
    lock boolean,
    category_id UUID,
    payee_id UUID,
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (payee_id) REFERENCES Payee(payee_id)
);

CREATE TABLE Monthly_Category (
    monthly_category_id UUID PRIMARY NOT NULL,
    month char(3),
    initial_balance float,
    activity float,
    assigned float,
    category_id UUID NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Category(category_id)
);
```
