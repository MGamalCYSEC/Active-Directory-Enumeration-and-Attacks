### 🔧 **Full Command**

```bash
dsquery * -filter "(&(objectCategory=user)(userAccountControl:1.2.840.113556.1.4.803:=2)(adminCount=1)(description=*))" -limit 5 -attr SAMAccountName description
```


## 🔍 **Section-by-Section Breakdown**

### ✅ `dsquery *`

- **`dsquery`**: A Windows command-line tool that queries Active Directory.
    
- **`*`**: Search **all objects** in the directory (not just users, groups, or OUs). You're using a **generic LDAP search**.
    
    > This allows you to use raw LDAP filters to precisely define what you're looking for.

### ✅ `-filter "(&(...))"`

This is the **LDAP filter** — the most important part.

The filter follows this structure:

```ldap
(&
   (filter1)
   (filter2)
   ...
)
```

The `&` means **AND**, so all conditions must match.

Let’s go inside:

#### ➤ `(objectCategory=user)`

- Matches **user objects** only (not groups, computers, etc.).
    
- Filters the query to only users in the directory.
    

#### ➤ `(userAccountControl:1.2.840.113556.1.4.803:=2)`

- This uses the **bitwise AND matching rule** (`1.2.840.113556.1.4.803`).
    
- You're checking whether the **bit for 'disabled accounts' (2)** is set in the `userAccountControl` attribute.
    
- **Purpose**: Find **disabled** user accounts.


#### ➤ `(adminCount=1)`

- `adminCount=1` is **automatically set** by AD on protected accounts.
    
- These are accounts that are members of **privileged groups** like:
    
    - Domain Admins
        
    - Enterprise Admins
        
    - Administrators
        
- **Purpose**: Only include **protected/privileged users**.
    

---

#### ➤ `(description=*)`

- The `*` wildcard means: the **description attribute exists and is not empty**.
    
- **Purpose**: Only return users who have a non-blank `description`.

### ✅ `-limit 5`

- Limits the result to **5 entries maximum**.
    
- Useful to speed up queries or avoid information overload during testing.


### ✅ `-attr SAMAccountName description`

- Selects which **attributes to display** in the output.
    
- In this case:
    
    - `sAMAccountName` → the user’s login name
        
    - `description` → the user’s description (if set)

## 📌 **Summary of What This Command Does**

> 🔍 _Find up to 5 disabled user accounts (`userAccountControl:...:=2`) that:_
> 
> - Are **user objects**
>     
> - Have `adminCount=1` (privileged)
>     
> - Have a **non-empty description**
>     
> 
> 🧾 _Display only their `sAMAccountName` and `description`_


## 💡 **Structure to Build Similar Commands**

```bash
dsquery * -filter "(&
   (objectCategory=user)
   (userAccountControl:1.2.840.113556.1.4.803:=<flag>)
   (otherAttribute=value)
   (anotherAttribute=*)
)" -limit <N> -attr <attribute1> <attribute2>
```

### You can change:

- `objectCategory` to `group`, `computer`, etc.
    
- Use other OIDs like:
    
    - `1.2.840.113556.1.4.804` → bitwise OR
        
- Add filters like:
    
    - `(name=*admin*)`
        
    - `(whenCreated>=20240701000000.0Z)` → recent objects
