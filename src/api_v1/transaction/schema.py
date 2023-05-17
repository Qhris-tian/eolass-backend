from enum import Enum


class TransactionTypeEnum(Enum):
    sale = "SALE"
    deposit = "DEPOSIT"
    withdraw = "WITHDRAW"
    auction_edit_fee = "AUCTION_EDIT_FEE"
    purchase = "PURCHASE"
    purchase_wallet_portion = "PURCHASE_WALLET_PORTION"
    gift_cards_purchase = "GIFT_CARDS_PURCHASE"
    exchange = "EXCHANGE"
    affiliate = "AFFILIATE"
    affiliate_payout = "AFFILIATE_PAYOUT"
    fee = "FEE"
    new_auction_fee = "NEW_AUCTION_FEE"
