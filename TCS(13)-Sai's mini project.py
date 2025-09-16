def sai_mini_project():
    initial_balance = int(input().strip())
    n = int(input().strip())

    balance = initial_balance
    transactions = []  # uncommitted transactions
    commits = []       # history of committed balances

    outputs = []

    for _ in range(n):
        parts = input().strip().split()
        op = parts[0]

        if op == "read":
            outputs.append(str(balance))

        elif op == "credit":
            amount = int(parts[1])
            balance += amount
            transactions.append(("credit", amount))

        elif op == "debit":
            amount = int(parts[1])
            balance -= amount
            transactions.append(("debit", amount))

        elif op == "abort":
            idx = int(parts[1]) - 1  # transaction index
            if 0 <= idx < len(transactions):
                t_type, amount = transactions[idx]
                # Undo the transaction
                if t_type == "credit":
                    balance -= amount
                else:  # debit
                    balance += amount
                # Remove transaction
                transactions.pop(idx)

        elif op == "commit":
            commits.append(balance)
            transactions.clear()

        elif op == "rollback":
            idx = int(parts[1]) - 1  # commit index
            if 0 <= idx < len(commits):
                balance = commits[idx]
                transactions.clear()

    print("\n".join(outputs))
