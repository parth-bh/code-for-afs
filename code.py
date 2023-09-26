import pandas as pd
import numpy as np

df = pd.read_csv("master_data.csv")
df['email'] = df.email.str.lower()

null_emailColumn = df[df.email.isnull()==True].shape

print("Total Students from Main Sheet based on email : ", df.shape[0])

print("Total Unique Students from Main Sheet based on email : ", df.email.unique().shape[0])

df_pass = pd.read_csv("pass_students.csv")
df_pass['email'] = df_pass.email.str.lower()

email_pass = list(df_pass.email)
if (len(set(email_pass))==len(email_pass)):
    print("No duplicate email in passed students.")
i=0

index_email = []
for ind in df.index:
    if df['email'][ind] in email_pass:
        index_email.append(ind)
        i+=1

print("Number of Passed Students based on email : ", len(email_pass))

print("Number of passed students matched with main sheet based on email : ", i)
df.drop(index_email, axis=0, inplace=True)

print(df.shape)


df.to_csv("output.csv")
print("File Saved.")