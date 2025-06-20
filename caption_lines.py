import random

def get_caption_lines():
    links = [
        "🐦 [Twitter](https://twitter.com/HashCoinFarm)",
        "🛒 [Inventory](https://hashcoin.farm/shop)",
        "💬 Forum: @ChainInside",
        "🎮 [Discord](https://discord.com/invite/D55sWhNgcb)"
    ]

    slogans = [
        "📜 #Hold Role — awarded for holding 10,000+ $HASH",
        "📜 Choose your role in the guild: guild.xyz/hashcoin",
        "📜 80% of all $HASH is distributed through mining",
        "📜 NFT role is limited — only 5,000 CAT (rare)",
        "📜 #Farm Role — for NFT GPU holders",
        "📜 Mining Hash — earn tokens through quests and activity",
        "🧪 Look Hook is testing new Web3 interaction formats",
        "🎁 No presale, no KYC — $HASH is earned through activity",
        "🛠 Look Hook products use $HASH within the ecosystem",
        "📉 HASH token has a limited supply",
        "📜 Purchased NFTs impact the liquidity of Hash Coin",
        "📜 All community members will receive an airdrop"
    ]

    chosen_link = random.choice(links)
    chosen_slogan = random.choice(slogans)

    return [
        chosen_link,
        chosen_slogan
    ]
