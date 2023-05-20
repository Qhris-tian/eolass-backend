def get_transaction_query(type):
    return {
        "query": """
            {
                B_transactions(types: [%s], status: COMPLETE, first: 5) {
                    totalCount
                    pageInfo {
                    hasNextPage
                    hasPreviousPage
                    startCursor
                    endCursor
                    }
                    edges {
                    node {
                        ... on B_API_SaleTransaction {
                        orderNumber
                        presale
                        referenceName
                        keyId
                        }
                        code
                        type
                        status
                        direction
                        money {
                        amount
                        currency
                        }

                        createdAt
                    }
                    cursor
                    }
                }
            }
        """
        % (type.value)
    }
