# Understanding Database ACID Properties: Atomicity and Durability

ACID is a set of properties that guarantee reliable transaction processing in database systems. Atomicity ensures that a transaction is treated as a single, indivisible unit of work; either all operations within the transaction are completed successfully, or none of them are. Durability guarantees that once a transaction has been committed, it will remain so, even in the event of system failures, power outages, or network issues. These properties are crucial for maintaining data integrity and consistency, especially in critical applications like financial systems.

## Key Takeaways
- Atomicity treats transactions as all-or-nothing operations, preventing partial updates.
- Durability ensures committed data is permanent and recoverable.
- Together, they form the foundation for reliable and consistent data management.

## Code Example
Consider a simple banking transaction to transfer money:

```python
import sqlite3

def transfer_funds(from_account_id, to_account_id, amount):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()

    try:
        # Start transaction (implicit in many DBs, explicit here for clarity)
        conn.execute("BEGIN TRANSACTION;")

        # Debit from account
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_account_id))
        if cursor.rowcount == 0:
            raise ValueError("Source account not found or insufficient funds.")

        # Credit to account
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_account_id))
        if cursor.rowcount == 0:
            raise ValueError("Destination account not found.")

        # Commit transaction
        conn.commit()
        print(f"Transfer of {amount} from {from_account_id} to {to_account_id} successful.")

    except Exception as e:
        # Rollback transaction on any error
        conn.rollback()
        print(f"Transaction failed: {e}. Rolling back.")
    finally:
        conn.close()

# Example usage (assuming a 'accounts' table exists with 'id' and 'balance' columns)
# transfer_funds(1, 2, 100)
```

---
*Logged on 2023-10-27 10:30:00 (UTC)*
