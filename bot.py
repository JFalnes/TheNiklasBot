# Author:       F4lnes
# Created:      09.04.2020

# Niklas-Bot Source Code
# If found, return to owner
from cryptocompare import cryptocompare
import asyncio
import shutil
import threading
import time
import youtube_dl as youtube_dl
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
import praw
import pokepy
import pyjokes
import requests
import json
from gtts import gTTS

load_dotenv()
# change these variables in your .env file to point to the right tokens or paths
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
REDDIT_ID = os.getenv('REDDIT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
FOLDER_PATH = os.getenv('FOLDER_PATH')
FFMPEG_PATH = os.getenv('FFMPEG_PATH')

folder = FOLDER_PATH
ffmpeg_ex = FFMPEG_PATH
PREFIX = '!'
VERSION = '1.0'
CHANGELOG = f'Version {VERSION} contains multiple bugfixes, QoL changes and some new features:\n' \
            f'1. !gamble, start a betting match with your friends! \n' \
            f'2. !clean, for administrators. Keep your discord neat and tidy!\n' \
            f'As always, every version contains multiple bugfixes to make Niklas work harder to please you'

bot = commands.Bot(command_prefix='!')

client = discord.Client()

r = praw.Reddit(client_id=REDDIT_ID,
                client_secret=REDDIT_SECRET,
                user_agent='<console:myFirstBot:1.0 (by /u/user)>', username='', password="")

# phrases the bot will say when posting a meme from reddit, change as you want
list_of_stealing = ['aggressively stolen from', 'willfully given to Niklas by', 'forcefully taken from',
                    'confiscated from', 'confiscated, for the good of the realm from']

# change or update this list to what you want
sub_list = ['memes', 'blackpeopletwitter', 'whitepeopletwitter', 'meirl', 'WholesomeMemes',
            'prequelmemes', 'lotrmemes', 'historymemes', 'comedycemetery', 'comedyheaven']

list_of_ball = ['As I see it, yes', 'Ask again later.', 'Better not tell you now.', ' Cannot predict now.',
                'Concentrate and ask again.', 'Don’t count on it.', 'It is certain.', 'It is certain.',
                'It is decidedly so.', 'Most Likely.', 'My reply is no.', 'My sources say no.',
                'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.',
                'Very doubtful.', ' Without a doubt.', 'Yes.', 'Yes - definitely', 'You may rely on it.']


def eight_answer():
    response = random.choice(list_of_ball)
    return ':8ball:, ' + response


def crypto_price(crypto):
    crypto_list = ['NXT', 'BTCD', 'PPC', 'CRAIG', 'XBS', 'XPY', 'PRC', 'YBC', 'DANK', 'GIVE', 'KOBO', 'DT', 'CETI',
                   'SUP', 'XPD', 'GEO', 'CHASH', 'NXTI', 'WOLF', 'XDP', '2015', '42', 'AC', 'ACOIN', 'AERO', 'ALF',
                   'AEGIS', 'AMC', 'ALIEN', 'APEX', 'ARCH', 'ARG', 'ARI', 'AXR', 'BET', 'BEAN', 'BLU', 'BOST', 'BQC',
                   'XMY', 'MOON', 'ZET', 'SXC', 'QTL', 'ENRG', 'RIC', 'DGC', 'LIMX', 'BTB', 'CAIX', 'BTMK', 'BUK',
                   'CACH', 'CANN', 'CAP', 'CASH', 'CAT', 'CBX', 'CCN', 'CIN', 'CINNI', 'CXC', 'CLAM', 'CLR', 'CMC',
                   'CNC', 'CNL', 'COMM', 'COOL', 'CRACK', 'CRYPT', 'CSC', 'DEM', 'DIAM', 'DRKC', 'DSB', 'DVC', 'EAC',
                   'EFL', 'ELC', 'EMD', 'EXCL', 'EXE', 'EZC', 'FLAP', 'FC2', 'FFC', 'FIBRE', 'FRC', 'FLT', 'FRK',
                   'FRAC', 'FSTC', 'GDC', 'GLC', 'GLD', 'GLX', 'GLYPH', 'GML', 'GUE', 'HAL', 'HBN', 'HUC', 'HVC', 'HYP',
                   'ICB', 'IFC', 'IXC', 'JBS', 'JKC', 'JUDGE', 'KDC', 'KEYC', 'KGC', 'LK7', 'LKY', 'LSD', 'LTB', 'LTCD',
                   'LTCX', 'LXC', 'LYC', 'MAX', 'MED', 'MINRL', 'MINT', 'MN', 'MINC', 'MRY', 'MZC', 'NAN', 'NAUT',
                   'NBL', 'NET', 'NMB', 'NRB', 'NOBL', 'NRS', 'NVC', 'NYAN', 'ORB', 'OPSC', 'PHS', 'POINTS', 'POT',
                   'PSEUD', 'PXC', 'PYC', 'RIPO', 'RPC', 'RT2', 'RYC', 'RZR', 'SAT2', 'SBC', 'SDC', 'SFR', 'SHADE',
                   'SHLD', 'SILK', 'SLG', 'SMC', 'SOLE', 'SPA', 'SPOTS', 'SRC', 'SSV', 'SUPER', 'SWIFT', 'SYNC', 'TAG',
                   'TAK', 'TES', 'TGC', 'TIT', 'TOR', 'TRC', 'TITC', 'ULTC', 'UNB', 'UNO', 'URO', 'USDE', 'UTC', 'UTIL',
                   'VDO', 'VOOT', 'VRC', 'WDC', 'XAI', 'XBOT', 'XC', 'XCR', 'XJO', 'XLB', 'XPM', 'XST', 'XXX', 'YAC',
                   'ZCC', 'ZED', 'EKN', 'XAU', 'TMC', 'SJCX', 'START', 'HUGE', 'XCP', 'MAID', '007', 'NSR', 'MONA',
                   'CELL', 'TEK', 'BAY', 'NTRN', 'SLING', 'XVC', 'CRAVE', 'XSI', 'BYC', 'GRC', 'GEMZ', 'KTK', 'HZ',
                   'FAIR', 'QORA', 'RBY', 'PTC', 'WBB', 'SSD', 'XTC', 'NOTE', 'FLO', 'MMXIV', '8BIT', 'STV', 'EBS',
                   'AM', 'XMG', 'AMBER', 'NKT', 'J', 'GHC', 'ABY', 'LDOGE', 'MTR', 'TRI', 'SWARM', 'BBR', 'BTCRY',
                   'BCR', 'XPB', 'XDQ', 'FLDC', 'SLR', 'SMAC', 'TRK', 'U', 'UIS', 'CYP', 'UFO', 'ASN', 'OC', 'GSM',
                   'FSC', 'NXTTY', 'QBK', 'BLC', 'MARYJ', 'OMC', 'GIG', 'CC', 'BITS', 'LTBC', 'NEOS', 'HYPER', 'VTR',
                   'METAL', 'PINK', 'GRE', 'XG', 'CHILD', 'BOOM', 'MINE', 'ROS', 'UNAT', 'SLM', 'GAIA', 'XTPL', 'FCN',
                   'XCN', 'CURE', 'GMC', 'MMC', 'XBC', 'CYC', 'OCTOC', 'MSC', 'EGGC', 'C2', 'GSX', 'CAMC', 'RBR', 'XQN',
                   'ICASH', 'NODET', 'SOON', 'BTMI', 'EVENT', '1CR', 'VIOR', 'XCO', 'VMC', 'MARSC', 'VIRAL', 'EQM',
                   'ISL', 'QSLV', 'XWT', 'XNA', 'RDN', 'SKB', 'BSTY', 'FCS', 'GAM', 'NXS', 'CESC', 'TWLV', 'EAGS',
                   'MLTC', 'ADC', 'MARS', 'XMS', 'SPHR', 'SIGU', 'M1', 'DB', 'CTO', 'EDGE', 'BITL', 'FUTC', 'GLOBE',
                   'TAM', 'MRP', 'CREVA', 'XFRC', 'NANAS', 'LOG', 'XCE', 'ACP', 'DRZ', 'BSC', 'DRKT', 'CIRC', 'NKA',
                   'VERSA', 'EPY', 'SQL', 'PIGGY', 'CHA', 'MIL', 'CRW', 'GEN', 'XPH', 'GRM', 'QTZ', 'ARB', 'LTS',
                   'SPINC', 'GP', 'BITZ', 'DUB', 'GRAV', 'BOBS', 'MNV', 'QCN', 'HEDGE', 'SONG', 'XSEED', 'AXIOM',
                   'SMLY', 'RBT', 'CHIP', 'SPEC', 'UNC', 'SPRTS', 'ZNY', 'BTQ', 'PKB', 'SNRG', 'GHOUL', 'HNC', 'DIGS',
                   'GCR', 'MAPC', 'MI', 'CON', 'TX', 'CLV', 'FCT', 'LYB', 'PXI', 'CPC', 'AMS', 'OBITS', 'CLUB', 'RADS',
                   'EMC', 'BLITZ', 'BHIRE', 'EGC', 'MND', 'I0C', 'BTA', 'NAS2', 'PAK', 'CRB', 'DOGED', 'OK', 'RVR',
                   'HYPERS', 'HODL', 'DGD', 'EDRC', 'HTC', 'DSH', 'DBIC', 'XHI', 'BIOS', 'CAB', 'DIEM', 'GBT', 'RCX',
                   'PWR', 'TRUMP', 'PRM', 'BCY', 'RBIES', 'BLRY', 'DOTC', 'SCOT', 'CREED', 'POSTC', 'INFX', 'ETHS',
                   'PXL', 'NUM', 'GOST', 'ION', 'GROW', 'UNITY', 'OLDSF', 'SSTC', 'NETC', 'GPU', 'TAGR', 'HMP', 'ADZ',
                   'GAPC', 'MYC', 'IVZ', 'VTA', 'SLS', 'SOIL', 'CUBE', 'YOC', 'VPRC', 'APC', 'STEPS', 'DBTC', 'UNIT',
                   'AEON', 'MOIN', 'ERC', 'AIB', 'PRIME', 'BERN', 'BIGUP', 'KR', 'XRE', '1337', 'PEPE', 'XDB', 'ANTI',
                   'BRK', 'COLX', 'MNM', 'ZEIT', '611', '2GIVE', 'CGA', 'SWING', 'SAFEX', 'NEBU', 'AEC', 'FRN', 'ADNT',
                   'PULSE', 'N7', 'CYG', 'LGBTQ', 'UTH', 'MPRO', 'KATZ', '404', 'SPM', 'MOJO', 'BELA', 'FLX', 'BOLI',
                   'CLUD', 'DIME', 'FLY', 'HVCO', 'GIZ', 'GREXIT', 'CARBON', 'DEUR', 'TUR', 'LEMON', 'DISK', 'NEVA',
                   'CYT', 'FUZZ', 'NKC', 'SECRT', 'XRA', 'XNX', 'STHR', 'BONES', 'WMC', 'GOTX', 'FLVR', 'SHREK', 'RISE',
                   'REVE', 'PBC', 'OBS', 'EXIT', 'EDUC', 'CLINT', 'CKC', 'VIP', 'NXE', 'ZOOM', 'DRACO', 'YOVI', 'ORLY',
                   'KUBOS', 'INCP', 'SAK', 'EVIL', 'OMA', 'MUE', 'COX', 'BNT', 'BSEND', 'DES', 'BIT16', 'PDC', 'CMTC',
                   'CHESS', 'SPACE', 'REE', 'LQD', 'MARV', 'XDE2', 'VEC2', 'OMNI', 'GSY', 'TRTK', 'LIR', 'MMNXT',
                   'SCRPT', 'LBC', 'SPCIE', 'STEEMD', 'CJ', 'PUT', 'KRAK', 'DLISK', 'IBANK', 'VOYA', 'ENTER', 'WRLGC',
                   'BM', 'FRWC', 'PSY', 'XTREME', 'RUST', 'NZC', 'SNGLS', 'XAUR', 'BFX', 'UNIQ', 'CRX', 'DCT', 'XPOKE',
                   'MUDRA', 'WARP', 'CNMT', 'PIZZA', 'LC', 'HEAT', 'ICN', 'EXB', 'WINGS', 'CDEX', 'RBIT', 'DCS.', 'KMD',
                   'GB', 'ANC', 'SYNX', 'MC', 'EDC', 'JWL', 'WAY', 'TAB', 'TRIG', 'BITCNY', 'BITUSD', 'ATMC', 'STO',
                   'SNS', 'CART', 'TOT', 'BTD', 'BOTS', 'MDC', 'FTP', 'ZET2', 'CVNC', 'KRB', 'TELL', 'ENE', 'TDFB',
                   'BLOCKPAY', 'BXT', 'ZYD', 'MST', 'GOON', '808', 'VLT', 'ZNE', 'DCK', 'COVAL', 'DGDC', 'TODAY', 'VRM',
                   'ROOT', '1ST', 'GPL', 'DOPE', 'B3', 'FX', 'PIO', 'PROUD', 'SMSR', 'UBIQ', 'ARM', 'ERB', 'LAZ',
                   'FONZ', 'BTCR', 'FCTC', 'SANDG', 'PUNK', 'MOOND', 'DLC', 'SEN', 'SCN', 'WEX', 'LTH', 'BRONZ', 'SH',
                   'BUZZ', 'MG', 'PSI', 'XPO', 'NLC', 'PSB', 'XBTS', 'FITC', 'PINKX', 'FIRE', 'UNF', 'SPORT', 'PPY',
                   'NTC', 'EGO', 'RCOIN', 'X2', 'MT', 'TIA', 'GBRC', 'XUP', '888', 'HALLO', 'BBCC', 'EMIGR', 'BHC',
                   'CRAFT', 'INV', 'OLYMP', 'DPAY', 'HKG', 'ANTC', 'JOBS', 'DGORE', 'THC', 'TRA', 'RMS', 'FJC', 'VAPOR',
                   'SDP', 'RRT', 'PREM', 'CALC', 'LEA', 'CF', 'CRNK', 'CFC', 'VTY', 'ARDR', 'BS', 'JIF', 'CRAB', 'HILL',
                   'MONETA', 'ECLIP', 'RUBIT', 'HCC', 'BRAIN', 'VTX', 'KRC', 'ROYAL', 'LFC', 'ZUR', 'NUBIS', 'TENNET',
                   'PEC', 'GMX', '32BIT', 'GNJ', 'TEAM', 'SCT', 'LANA', 'ELE', 'GCC', 'AND', 'EQUAL', 'SWEET', '2BACCO',
                   'DKC', 'COC', 'CHOOF', 'CSH', 'ZCL', 'RYCN', 'PCS', 'NBIT', 'WINE', 'DAR', 'IFLT', 'ZECD', 'ZXT',
                   'WASH', 'TESLA', 'LUCKY', 'VSL', 'TPG', 'LC4', 'MDT', 'CBD', 'PEX', 'INSANE', 'GNT', 'PENC', 'BASH',
                   'FAMEC', 'LIV', 'SP', 'MEGA', 'VRS', 'ALC', 'DOGETH', 'KLC', 'HUSH', 'BTLC', 'DRM8', 'FIST', 'EBZ',
                   '365', 'DRS', 'FGZ', 'BOSON', 'ATX', 'PNC', 'BRDD', 'TIME', 'BIPC', 'EMB', 'BTTF', 'DLR', 'CSMIC',
                   'SCASH', 'XEN', 'JIO', 'IW', 'JNS', 'TRICK', 'DCRE', 'FRE', 'NPC', 'PLNC', 'DGMS', 'ICOB', 'ARCO',
                   'KURT', 'XCRE', 'ENT', 'UR', 'MTLM3', 'ODNT', 'EUC', 'CCXC', 'BCF', 'SEEDS', 'XSN', 'TKS', 'BCCOIN',
                   'SHORTY', 'PCM', 'KC', 'CORAL', 'BamitCoin', 'NXC', 'MONEY', 'BSTAR', 'HSP', 'HZT', 'CRSP', 'XSPT',
                   'CCRB', 'BULLS', 'INCNT', 'ICON', 'NIC', 'ACN', 'XNG', 'XCI', 'LOOK', 'LOC', 'MMXVI', 'TRST', 'MIS',
                   'WOP', 'CQST', 'IMPS', 'IN', 'CHIEF', 'GOAT', 'ANAL', 'RC', 'PND', 'PX', 'OPTION', 'AV', 'LTD',
                   'UNITS', 'HEEL', 'GAKH', 'GAIN', 'S8C', 'LVG', 'DRA', 'ASAFE2', 'LTCR', 'QBC', 'XPRO', 'ASTR',
                   'GIFT', 'VIDZ', 'INC', 'PTA', 'ACID', 'ZLQ', 'RADI', 'RNC', 'GOLOS', 'PASC', 'TWIST', 'PAYP', 'DETH',
                   'YAY', 'YES', 'LENIN', 'MRSA', 'OS76', 'BOSS', 'MKR', 'BIC', 'CRPS', 'MOTO', 'NTCC', 'HXX', 'SPKTR',
                   'MAC', 'SEL', 'NOO', 'CHAO', 'XGB', 'YMC', 'JOK', 'GBIT', 'TEC', 'BOMBC', 'RIDE', 'KED', 'CNO',
                   'WEALTH', 'IOP', 'XSPEC', 'PEPECASH', 'CLICK', 'ELS', 'KUSH', 'ERY', 'PLU', 'PRES', 'BTZ', 'OPES',
                   'WCT', 'RATIO', 'BANC', 'NICEC', 'SMF', 'CWXT', 'TECH', 'CIR', 'LEPEN', 'ROUND', 'MARI', 'MARX',
                   'HAZE', 'PRX', 'NRC', 'PAC', 'IMPCH', 'ERR', 'TIC', 'NUKE', 'EOC', 'SFC', 'JANE', 'PARA', 'MM',
                   'CTL', 'NDOGE', 'ZBC', 'FRST', 'ORO', 'ALEX', 'TBCX', 'MCAR', 'THS', 'ACES', 'UAEC', 'EA', 'PIE',
                   'CREA', 'WISC', 'BVC', 'FIND', 'MLITE', 'STALIN', 'TSE', 'VLTC', 'BIOB', 'SWT', 'PASL', 'ZER',
                   'CHAT', 'NETKO', 'ZOI', 'HONEY', 'MXTC', 'MUSIC', 'DTB', 'VEG', 'MBIT', 'VOLT', 'EDG', 'B@', 'BESTC',
                   'CHC', 'ZENI', 'PLANET', 'DUCK', 'BNX', 'BSTK', 'RNS', 'DBIX', 'AMIS', 'KAYI', 'XVP', 'BOAT', 'TAJ',
                   'IMX', 'CJC', 'AMY', 'QBT', 'EB3', 'XVE', 'FAZZ', 'APT', 'BLAZR', 'ARPAC', 'UNIVRS', 'ECOC', 'XLR',
                   'DARK', 'DON', 'MER', 'WGO', 'RLC', 'ATMOS', 'ETT', 'VISIO', 'HPC', 'GIOT', 'CXT', 'EMPC', 'GNO',
                   'LGD', 'TAAS', 'BUCKS', 'XBY', 'MCRN', 'LUN', 'RAIN', 'WSX', 'IEC', 'IMS', 'ARGUS', 'CNT', 'LMC',
                   'BTCS', 'PROC', 'XGR', 'BENJI', 'HMQ', 'BCAP', 'DUO', 'RBX', 'GRW', 'APX', 'MILO', 'OLV', 'ILC',
                   'MRT', 'IOU', 'PZM', 'PHR', 'ANT', 'PUPA', 'RICE', 'XCT', 'DEA', 'REDCO', 'ZSE', 'CTIC', 'TAP',
                   'BITOK', 'PBT', 'MUU', 'INF8', 'HTML5', 'MNE', 'DICE', 'SBSC', 'USC', 'DUX', 'XPS', 'EQT', 'INSN',
                   'BAT', 'MNTC', 'F16', 'HAMS', 'NEF', 'BOS', 'QWARK', 'QRL', 'ADL', 'PTOY', 'ZRC', 'LKK', 'ESP',
                   'DYN', 'SEQ', 'MCAP', 'MYST', 'VERI', 'CFI', 'SNT', 'AVT', 'IXT', 'STA', 'TFL', 'EFYT', 'MCO', 'NMR',
                   'ADX', 'QAU', 'ECOB', 'PLBT', 'USDT', 'AHOO', 'ATB', 'TIX', 'CHAN', 'CMP', 'RVT', 'HRB', 'NIM',
                   '8BT', 'DAOACT', 'DNT', 'SUR', 'PING', 'MIV', 'DAOC', 'SAN', 'WGR', 'XEL', 'NVST', 'FUNC', 'WTT',
                   'HVN', 'MYB', 'SNC', 'STAR', 'COR', 'XRL', 'OROC', 'OAX', 'MBI', 'DDF', 'DIM', 'GGS', 'DNA', 'FYN',
                   'FND', 'DCY', 'CFT', 'D', 'DP', 'VUC', 'BTPL', 'UNIFY', 'BRIT', 'AMMO', 'SOCC', 'MASS', 'LA', 'IML',
                   'STU', 'PLR', 'GUNS', 'IFT', 'BCAT', 'SYC', 'IND', 'TRIBE', 'ZRX', 'TNT', 'COS', 'STORM', 'NPX',
                   'STORJ', 'SCORE', 'OTX', 'VOISE', 'ETBS', 'CVCOIN', 'DRP', 'ARC', 'BOG', 'NDC', 'POE', 'ADT', 'UET',
                   'PART', 'AGRS', 'BEACH', 'DAS', 'ADS', 'XCJ', 'RKC', 'NLC2', 'LINDA', 'KING93', 'ANCP', 'RCC',
                   'ROOTS', 'SNK', 'CABS', 'OPT', 'ZNT', 'BITSD', 'XLC', 'SKIN', 'MSP', 'HIRE', 'REAL', 'DFBT', 'EQ',
                   'WLK', 'VIB', 'ONION', 'BTX', 'ICE', 'XID', 'GCN', 'MANA', 'ICOO', 'TME', 'SIGT', 'ONX', 'COE',
                   'ARENA', 'WINK', 'CRM', 'DGPT', 'MOBI', 'CSNO', 'KICK', 'SDAO', 'STX', 'COREG', 'KEN', 'QVT', 'TIE',
                   'AUT', 'GRWI', 'MNY', 'MTH', 'CCC', 'UMC', 'BMXT', 'GAS', 'OCL', 'BNC', 'TOM', 'SMNX', 'DCN', 'DLT',
                   'MRV', 'MBRS', 'SUB', 'PGL', 'XMCC', 'AUN', 'CMPCO', 'DTCT', 'CTR', 'WNET', 'PRG', 'THNX', 'WORM',
                   'FUCK', 'VRD', 'SIFT', 'IGNIS', 'IWT', 'JDC', 'ITF', 'AIX', 'XEC', 'ENTRP', 'ICOS', 'PIX', 'MEDI',
                   'HGT', 'LTA', 'NIMFA', 'SCOR', 'MLS', 'KEX', 'COB', 'BRO', 'MINEX', 'ATL', 'DFT', 'UTK', 'LAT',
                   'SOJ', 'HDG', 'STCN', 'SQP', 'RIYA', 'LNK', 'AMB', 'MNTP', 'ALTOCAR', 'BKX', 'BOU', 'OXY', 'TTT',
                   'AMT', 'GIM', 'NYC', 'LBTC', 'FRAZ', 'EMT', 'GXC', 'HBT', 'KRONE', 'SRT', 'AVA', 'BT', 'ACC', 'Z2',
                   'LINX', 'XCXT', 'BLAS', 'SCL', 'TRVL', 'CRTM', 'EON', 'PRIX', 'CTX', 'ENJ', 'CNX', 'FUEL', 'ACE',
                   'WRC', 'BRX', 'UCASH', 'WRT', 'ORME', 'DEEPG', 'CCT', 'WSH', 'ARNA', 'ABC', 'PRP', 'BMC', 'SKRT',
                   '3DES', 'PYN', 'KAPU', 'SENSE', 'CAPP', 'VEE', 'FC', 'RCN', 'NRN', 'EVC', 'LINK', 'WIZ', 'ATKN',
                   'KNC', 'RUSTBITS', 'REX', 'ETHD', 'SUMO', 'H2O', 'TKT', 'RHEA', 'ART', 'DRT', 'SNOV', 'MTN',
                   'STOCKBET', 'PLM', 'SALT', 'SND', 'XP', 'GLA', 'ZNA', 'EZM', 'ODN', 'POLL', 'MTK', 'CAS', 'MAT',
                   'GJC', 'WIC', 'WEB', 'WAND', 'ELIX', 'EBTC', 'HAC', 'YOYOW', 'REC', 'BIS', 'OPP', 'ROCK2', 'EARTH',
                   'ICX', 'VSX', 'FLASH', 'GRFT', 'BTCZ', 'CZC', 'PPP', 'GUESS', 'CAN', 'CIX', 'ERT', 'FLIK', 'TRIP',
                   'MBT', 'JVY', 'ALIS', 'LEV', 'ARBI', 'REQ', 'ARNX', 'DAT', 'VIBE', 'ROK', 'XRED', 'DAY', 'AST',
                   'FLP', 'HXT', 'CND', 'VRP', 'NTM', 'TZC', 'MCI', 'COV', 'AIR', 'FUJIN', 'ATCC', 'KOLION', 'WILD',
                   'ELTC2', 'ILCT', 'POWR', 'C20', 'RYZ', 'ELM', 'TER', 'XCS', 'BQ', 'CLOUT', 'EVR', 'TOA', 'MNZ',
                   'VIVO', 'PHX', 'ZSC', 'AURS', 'CAG', 'PKT', 'ECHT', 'INXT', 'ATS', 'RGC', 'EBET', 'REV', 'MOD',
                   'BITCM', 'CPAY', 'RUP', 'BON', 'WHL', 'UP', 'ETG', 'WOMEN', 'MAY', 'RNDR', 'EDDIE', 'SOMA', 'NAMO',
                   'KCS', 'GAT', 'BLUE', 'FLLW', 'WYR', 'VZT', 'INDI', 'LUX', 'BAR', 'PIRL', 'ECASH', 'WPR', 'DRGN',
                   'ODMC', 'BRAT', 'DTR', 'TKR', 'ELITE', 'XIOS', 'DOV', 'REA', 'AVE', 'XNN', 'BTDX', 'LOAN', 'ZAB',
                   'BT1', 'BT2', 'SHARPE', 'JCR', 'XSB', 'ATM', 'EBST', 'KEK', 'AID', 'BLHC', 'ALTCOM', 'DATA', 'UGC',
                   'PLAY', 'PURE', 'CLD', 'OTN', 'POS', 'REBL', 'NEOG', 'EXN', 'XNS', 'TRCT', 'UKG', 'BTCRED', 'CPEX',
                   'JTX', 'AXT', 'NEU', 'RUPX', 'BDR', 'TIOX', 'HNCN', 'MADC', 'PURA', 'INN', 'HST', 'BCPT', 'BDL',
                   'CMS', 'XBL', 'ZEPH', 'ATFS', 'GES', 'PHORE', 'LCASH', 'CFD', 'SPHTX', 'PLC', 'WSC', 'DBET', 'XGOX',
                   'NEWB', 'LIFE', 'RMC', 'CREDO', 'MSR', 'CJT', 'EVN', 'BNK', 'ELLA', 'BPL', 'COIN', 'ROCK', 'DRXNE',
                   'SKR', 'GRID', 'XPTX', 'GVT', 'ETK', 'ASTRO', 'GMT', 'EMPH', 'SOAR', 'EXY', 'ISH', 'MNX', 'CRDS',
                   'VIU', 'SCRM', 'DBR', 'GFT', 'STAC', 'RIPT', 'BBT', 'GBX', 'CSTL', 'ICC', 'JNT', 'XLQ', 'KNGN',
                   'TRIA', 'PBL', 'MAG', 'STEX', 'UFR', 'LOCI', 'TAU', 'LAB', 'DEB', 'FLIXX', 'FRD', 'PFR', 'ECA',
                   'LDM', 'LTG', 'STP', 'SPANK', 'WISH', 'AERM', 'PLX', 'AUTON', 'ETHB', 'CDX', 'FOOD', 'DEC', 'VOT',
                   'UQC', 'LEND', 'SETHER', 'XSH', 'GEA', 'BCO', 'DSR', 'BDG', 'ONG', 'PRL', 'BTCM', 'ETBT', 'ZCG',
                   'MUT', 'DIVX', 'CNBC', 'RHOC', 'XUN', 'RFL', 'COFI', 'ELTCOIN', 'GRX', 'NTK', 'ERO', 'RLX', 'MAN',
                   'CWV', 'NRO', 'SEND', 'GLT', 'X8X', 'COAL', 'DAXX', 'BWK', 'FNTB', 'XMRG', 'BTCE', 'FYP', 'BOXY',
                   'NGC', 'UTNP', 'EGAS', 'DPP', 'ADB', 'TGT', 'BMT', 'BIO', 'MTRC', 'BTCL', 'PCN', 'PYP', 'CRED',
                   'SBTC', 'KLKS', 'AC3', 'CHIPS', 'HKN', 'B2B', 'LOCK', 'LTHN', 'GER', 'LTCU', 'MGO', 'BTCA', 'HQX',
                   'STAK', 'BCOIN', 'MEDIB', 'CCOS', 'BNTY', 'BRD', 'HAT', 'ELF', 'VLR', 'CWX', 'DBC', 'ZP', 'POP',
                   'CRC', 'PNX', 'BAS', 'UTT', 'AMM', 'XCPO', 'GET', 'ERC20', 'HTML', 'GENE', 'NMS', 'PHO', 'XTRA',
                   'NTWK', 'SUCR', 'ACCO', 'BYTHER', 'REM', 'TOK', 'EREAL', 'CPN', 'XFT', 'QLC', 'BSE', 'OMGC', 'Q2C',
                   'BLT', 'SPF', 'TDS', 'ORE', 'SPK', 'GOA', 'WAGE', 'GUN', 'DFS', 'POLIS', 'WELL', 'FLOT', 'CL',
                   'SHND', 'AUA', 'DNN', 'SAGA', 'TSL', 'IRL', 'BODHI', 'PMA', 'TROLL', 'FORCEC', 'SUGAR', 'JET', 'MDS',
                   'LCP', 'GTC', 'IETH', 'TGCC', 'SDRN', 'INK', 'KBR', 'MONK', 'MGN', 'KZC', 'GNR', 'LNC', 'LWF',
                   'BRIC', 'WCG', 'BHIVE', 'GX', 'LCK', 'MFG', 'ETL', 'TEL', 'DRG', 'SPX', 'ONL', 'ZAP', 'AIDOC', 'ECC',
                   'ET4', 'LCT', 'EBC', 'VESTA', 'INT', 'CPY', 'STEN', 'SFU', 'PCOIN', 'BLNM', 'LUC', 'EDT', 'CYDER',
                   'SRNT', 'MLT', 'EKO', 'UBTC', 'BTO', 'DOCC', 'ARCT', 'IMVR', 'IDEX', 'IDH', 'CBT', 'ITZ', 'XBP',
                   'EXRN', 'LGO', 'CRPT', 'SGL', 'TNC', 'FSBT', 'CFTY', 'DTA', 'CV', 'DTX', 'MCU', 'OCN', 'THETA',
                   'PRPS', 'DUBI', 'BPT', 'SGN', 'TRAC', 'MOT', 'HORSE', 'QBAO', 'ACCN', 'SWFTC', 'SENT', 'IPL', 'OPC',
                   'SAF', 'SHA', 'PYLNT', 'GRLC', 'EVE', 'REPUX', 'JOYT', 'CAPD', 'BTW', 'AXPR', 'FOTA', 'DDD', 'CPCH',
                   'SPEND', 'ZPT', 'REF', 'SXDT', 'SXUT', 'LDC', 'VAL', 'MXAI', 'BCDN', 'STK', 'MZX', 'CRYC', 'Q1S',
                   'POLY', 'XTO', 'TPAY', 'CXO', 'WT', 'HGS', 'SISA', 'EBIT', 'RCT', 'CUZ', 'HLC', 'BETR', 'GMR', 'ING',
                   'LHC', 'BLZ', 'CVNG', 'CHSB', 'EQUI', 'MCT', 'HHEM', 'CWIS', 'GRO', 'SWM', 'MDCL', 'WOBTC', 'DNO',
                   'eFIC', 'TKY', 'BANCA', 'TRTL', 'DRPU', 'DOR', 'PRFT', 'PARETO', 'DTRC', 'NDLC', 'BEE', 'MUN', 'TIG',
                   'LYK', 'NYX', 'DXT', 'SAT', 'CRL', 'ORI', 'LYM', 'USX', 'LGR', 'BCA', 'B2X', 'EXMR', 'UETL', 'NBR',
                   'ARY', 'RAVE', 'ILT', 'SCOOBY', 'CEFS', 'BUN', 'BSR', 'SKULL', 'TRDT', 'XBTY', 'JC', 'BTCP', 'SKC',
                   'MWAT', 'JEW', 'ERIS', 'KRM', 'HT', 'CDY', 'SSS', 'CRDNC', 'BIFI', 'CADN', 'BTF', 'IPC', 'SHOW',
                   'STC', 'AIT', 'STQ', 'ALT', 'CXP', 'KB3', 'FDX', 'KREDS', 'EQL', 'GAI', 'VULC', 'CTC', 'DVTC',
                   'DADI', 'MGGT', 'TOKC', 'UNRC', 'BBP', 'NOX', 'HYS', 'LCWP', 'NAVI', 'ADI', 'VVI', 'ANKORUS', 'IVC',
                   'HLP', 'VIN', 'SHPING', 'PTR', 'LCC', 'VANY', 'TFD', 'NOXB', 'BAX', 'BERRY', 'APCC', 'FLIP', 'CLIN',
                   'GOOD', 'ENK', 'ALX', 'REN', 'DTH', 'SOC', 'TDX', 'LOTTO', 'FUNK', 'LEAF', 'COMPD', 'BITCAR', 'CLN',
                   'ORYX', 'BASHC', 'DIGIF', 'DGM', 'CBS', 'TERN', 'SVD', 'PROOF', 'BTCH', 'redBUX', 'AUC', 'LIZ',
                   'CIF', 'NCASH', 'SPD', 'CMCT', 'RPUT', 'FILL', 'XNK', 'XYO', 'PROPS', 'CEDEX', 'FUNDP', 'CEL',
                   'CRDTS', 'PUSHI', 'BINS', 'POKER', 'AXYS', 'EVENC', 'BOLD', 'EXTN', 'DIG', 'ETS', 'LIPC', 'GOFF',
                   'HELL', 'ELP', 'ACAT', 'RKT', 'ELI', 'CO2', 'INVOX', 'ACTN', 'LTCH', 'ZUP', 'USCOIN', 'KIND', 'BCHT',
                   'CLO', 'CURI', 'ELIC', 'MOAT', 'BBI', 'BEZ', 'ENTRC', 'BTCGO', 'XTROPTIONS', 'KNW', 'PGC', 'BIT',
                   'DATX', 'PKC', 'SQOIN', 'TBAR', 'TAN', 'CPL', 'TUBE', 'AUTO', 'OMX', 'TRCK', 'TOMO', 'XAYA', 'MBM',
                   'INVC', 'W3C', 'DIN', 'INSTAR', 'CHP', 'PSD', 'J8T', 'LELE', 'DROP', 'AKA', 'SHIP', 'IHT', 'LCS',
                   'LALA', 'LEDU', 'FOXT', 'ETKN', 'ROX', 'ADM', 'AMBT', 'BTRM', 'MANNA', 'ePRX', 'HMC', 'ZIX', 'ELEC',
                   'ORGT', 'PAN', 'BOTC', 'VIEW', 'OKOIN', 'ADK', 'ESS', 'VIT', 'SERA', 'BLN', 'AET', 'CMOS', 'PGN',
                   'BMH', 'REDN', 'TLP', 'GENS', 'BSX', 'BBN', 'TDZ', 'PAVO', 'TUSD', 'LDN', 'BUBO', 'USOAMIC', 'FLUZ',
                   'IPSX', 'MIO', 'AIC', 'MITH', 'BNN', 'SPND', 'FNO', 'PAS', 'XSG', 'CVTC', 'PLMT', 'NEXT', 'RNTB',
                   'XCLR', 'BPX', 'SWTH', 'FDZ', 'VTN', 'LION', 'MASP', 'XTL', 'UCN', 'HUR', 'BRIA', 'IC', 'LATX',
                   'ROI', 'ETHPR', 'MNB', 'ACHC', 'BTL', 'GOAL', 'RAC', 'BEX', 'HOLD', 'EZT', 'SOL', 'VIC', 'XCM',
                   'NFN', 'CEEK', 'WIIX', 'EOSDAC', 'BCI', 'MEDIC', 'BBCT', 'KWH', 'VLD', 'FTX', 'GSI', 'BDP', 'FLMC',
                   'ALPS', 'ZEL', 'BKC', 'BITG', 'DEV', 'CHT', 'GREEN', 'ABJ', 'FTW', 'RAP', 'ARTE', 'ANI', 'PHC',
                   'ETHM', 'UBC', 'NOKU', 'SENC', 'PAT', 'LIGER', 'CHFN', 'EURN', 'LEU', 'SWC', 'ORS', 'SEM', 'DARX',
                   'BBK', 'NCT', 'UWC', 'UUU', 'XHV', 'CPX', 'EQC', 'ADH', 'ZLA', 'LIF', 'EFX', 'LND', 'MNRB', 'FTO',
                   'HPAY', 'SIG', 'CARE', 'NZL', 'TBT', 'XMC', 'OAK', 'DML', 'GEM', 'TIPS', 'MOS', 'TBX', 'PENTA',
                   'WCOIN', 'CHARM', 'PROTON', 'DERO', 'DEAL', 'JUMP', 'ZCO', 'KRL', 'TRAXIA', 'NEXO', 'CHX', 'SS',
                   '0XBTC', 'XMO', 'EDU', 'PCL', 'APH', 'NBAI', 'CVT', 'TUT', 'BETT', 'NOAH', 'PAL', 'ENU', 'BFDT',
                   'KEP', 'RUBY', 'CTKN', 'YUM', 'GSC', 'DESI', 'FNP', 'VLUX', 'MTC', 'MTKN', 'SSH', 'XBI', 'VRA',
                   'TRUE', 'MRK', 'FRV', 'WINS', 'XES', 'RTB', 'FXT', 'DXC', 'CHBR', 'OWD', 'ELLI', 'DAN', 'CSEN',
                   'UBT', 'AMO', 'LIVE', 'GBG', 'CNN', 'SHL', 'ETZ', 'SKM', 'SHR', 'UBEX', 'IVY', 'KEC', 'ODE', 'AMN',
                   'SABR', 'HWC', 'BITGOLD', 'BITSILVER', 'GIN', 'OPEN', 'NLX', 'LNKC', 'FACE', 'MRPH', 'IOTX', 'STM',
                   'ITL', 'AITT', 'ITM', 'VID', 'UCT', 'SNTR', 'ZMR', 'XMV', 'NKN', 'ELY', 'HER', 'PARLAY', 'SLX',
                   'LTCC', 'RST', 'XBB', 'AMX', 'TFC', 'REPO', 'IRC', 'PLATC', 'OIO', 'ANGL', 'ANTS', 'KNG', 'CMM',
                   'STT', 'WYS', 'COG', 'ZIPT', 'QKC', 'OSA', 'EXC', 'BEN', 'BCIO', 'BMK', 'ROC', 'BZNT', 'LYL', 'PHI',
                   'PMNT', 'BNTN', 'HYT', 'SOUL', 'GRMD', 'SSC', 'BKT', 'NCP', 'MPT', 'STAX', 'MRN', 'FOPA', 'CBC',
                   'OOT', 'NBC', 'SIC', 'ALG', 'PI', 'EXCC', 'REL', 'BTCN', 'HERO', 'EJAC', 'APIS', 'XT3', 'MGD', 'VIG',
                   'PLURA', 'SWACH', 'NWCN', 'EMAR', 'ICST', 'XTNC', 'ROE', 'LTCP', 'DKD', 'LYNX', 'POSQ', 'YCE', 'OCX',
                   'STOR', 'ARO', 'BWS', 'BTCC', 'GOLF', 'MUSE', 'OCT', 'XCEL', 'ECH', 'XMN', 'PLUS1', 'COI', 'CANDY',
                   'AXE', 'SHARD', 'GMCN', 'TRVC', 'KRX', 'BITX', 'SKRB', 'HFT', 'OOW', 'DTEM', 'TIP', 'SOUND', 'HB',
                   'TRW', 'IQN', 'GIC', 'EPIK', 'SPARTA', 'ZMN', 'PNY', 'SAFE', 'COU', 'ATH', 'ABS', 'VITAE', 'XET',
                   '0xDIARY', 'BSPM', 'TDP', 'XGS', 'XUEZ', 'BIM', 'WORX', 'Dow', 'HEXC', 'PYT', 'DEI', 'TPC', 'OYS',
                   'WEBC', 'JEX', 'ILK', 'RYO', 'MUSD', 'MIC', 'URALS', 'QWC', 'WAB', 'BITN', 'ARE', 'DACASH', 'EUNO',
                   'KAAS', 'MMO', 'DASC', 'PGTS', 'MEDX', 'CET', 'SLST', 'TGAME', 'SPN', 'ZINC', 'KETAN', 'KBC',
                   'INSUR', 'NIX', 'ZCN', 'RPM', 'DGX', 'ITA', 'NOM', 'XSTC', 'U42', 'EGCC', 'FREC', 'DCC', 'AURO',
                   'MOTI', 'PPAI', 'MIXI', 'CBRT', 'MEET', 'BOE', 'RTE', 'CAR', 'CPT', 'PCO', 'XPST', 'HSC', 'MCV',
                   'SCRL', 'CONI', 'XPAT', 'MBLC', 'DIW', 'JOINT', 'IDXM', 'CCO', 'ATMI', 'TKA', 'RMT', 'OLT', 'GETX',
                   'IQ', 'BWT', 'EMV', 'ESZ', 'TRAK', 'ZXC', 'BTRN', 'XMX', 'VME', 'PERU', 'VITE', 'RNT', 'BBO', 'YUP',
                   'SNIP', 'XDNA', 'SAL', 'RPL', 'CARD', 'LIKE', 'THRT', 'GTK', 'SKRP', 'AVH', 'SCC', 'HALO', 'BSTN',
                   'PITCH', 'NANJ', 'PAXEX', 'DIT', 'AZART', 'CENNZ', 'RDC', 'TTU', 'FREE', 'AOP', 'XAP', 'INTO', 'RED',
                   'AIMS', 'TSC', 'SEER', 'SPLB', 'CMZ', 'NOBS', 'HMN', 'MHP', 'HMD', 'JSE', 'IMGZ', 'NYN', 'IAM',
                   'URB', 'CHART', 'WHEN', 'SFT', 'ORBIS', 'BLKS', 'ETRNT', 'ITR', 'CHE', 'ZEEW', 'MEM', 'QUA', 'RSC',
                   'ENTRY', 'PHTC', 'WORK', 'ORC', 'ZAZA', 'DNET', 'IDAP', 'HEAL', 'OFCR', 'SHPT', 'LED', 'PRLPAY',
                   'RBDT', 'SKYFT', 'TFLEX', 'STRY', 'FAN', 'GBTC', 'NBOX', 'BUD', 'DBCCOIN', 'K2G', 'ARR', 'GAMB',
                   'SPOT', 'VTUUR', 'ETI', 'FRECNX', 'NOIA', 'LAX', 'BOO', 'DREAM', 'PTI', 'LPC', 'DYNO', 'MFX', 'NOIZ',
                   'SPIKE', 'SGO', 'RAWG', 'BDB', 'MNR', 'ZNAQ', 'YBT', 'OPET', 'PSK', 'KVT', 'COT', 'WPT', 'ABELE',
                   'XEP', 'ARBT', 'OMI', 'BILL', 'ST', 'WBBC', 'XDT', 'WPP', 'ASTO', 'SLT', 'APL', 'HDAC', 'CCCX',
                   'VRH', 'AEN', 'SOLID', 'VANIG', 'AIRE', 'GMA', 'WMB', 'MVU', 'TLNT', 'GLDR', 'IMU', 'TRT', 'CRS',
                   'YON', 'URT', 'QCX', 'CRON', 'DIP', 'PROD', 'REDC', 'ZCHN', 'TTV', 'OICOIN', 'ENQ', 'DTN', 'IDM',
                   'SIDT', 'ISR', 'CDPT', 'CRGO', 'AXIS', 'QRP', 'TIIM', 'BNR', 'VRT', 'ZCC1', 'KRP', 'OLE', 'OKB',
                   'AMLT', 'HGO', 'TCOIN', 'BZ', 'PRA', 'VLP', 'ZIP', 'BTK', 'KCASH', '1WO', 'ZB', 'BOUTS', 'EST',
                   'MODEX', 'OGT', 'PLA', 'NPER', 'ATON', 'EURS', 'XCG', 'BOONS', 'PCH', 'ECOM', 'WIT', 'OPU', 'ETALON',
                   'TICS', 'ZPR', 'EXLT', 'ESTATE', 'BLV', 'RRC', 'MPG', 'QNTU', 'IG', 'FML', 'TLU', 'PSM', 'MON',
                   'AUDC', 'NMH', 'KST', 'DEL', 'HIT', 'PBLK', 'KVNT', 'MDN', 'TMTG', 'PRT', 'COSM', 'GPPT', 'LNL',
                   'VRN', 'BRNX', 'SRCOIN', 'RFT', 'ET', 'MMTM', 'XGH', 'FXP', 'DICEM', 'PASS', 'HRO', 'DGTX', 'BSCH',
                   'TRVR', 'PESA', 'CLPX', 'DAOX', 'GLN', 'AUK', 'PCCM', 'TOPC', 'PLAN', 'EVER', 'TRAID', 'BNTE', 'DPY',
                   'FUNDZ', 'MIB', 'BAAS', 'LYNK', 'TBC', 'CCL', 'HYC', 'TCX', 'HLD', 'DACC', 'NUSD', 'TCHB', 'DAX',
                   'BECH', 'VEEN', 'CIC', 'MIODIO', 'MOV', 'IHF', 'CNAB', 'SGP', 'LTPC', 'HANA', 'BTV', 'URP', 'SHE',
                   'IVN', 'DAV', 'ZAT', 'IMT', 'MHC', 'ROBET', 'CRYP', 'BONIX', 'BTXC', 'DAPS', 'ETE', 'NHCT', 'AZ',
                   'SWA', 'USDCT', 'IAG', 'STRS', 'MTCMN', 'AAA', 'ZEST', 'HLM', 'CSP', 'USDC', 'ONGAS', 'NRVE', 'BIP',
                   'XCASH', 'RMESH', 'HAND', 'GBXT', 'ABCC', 'BASIS', 'JIB', 'PMTN', 'SGR', 'PHM', 'CUSD', 'KUSD',
                   'VEOT', 'GGR', 'VEST', 'MCN', 'TCH', 'DEPO', 'MENLO', 'TVA', 'METM', 'PAX', 'ARAW', 'BRAZ', 'TALAO',
                   'IZX', 'DIVI', 'HQT', 'W12', 'NBAR', 'KBX', 'MYDFS', 'VTHO', 'BHPC', 'VTOS', 'M2O', 'SLY', 'UEC',
                   'BEAT', 'MOLK', 'MSD', 'SEED', 'SEALN', 'GBO', 'ACM', 'DFXT', 'BF', 'NWP', 'BCDT', 'EVOS', 'DEEX',
                   'ANON', 'LTZ', 'MTZ', 'TBL', 'BXY', 'KUE', 'ESN', 'H3O', 'BETHER', 'ETHO', 'WTL', 'HIH', 'ANGEL',
                   'P2PS', 'AIM', 'TWISTR', 'CXA', 'BITTO', 'UMK', 'VNX', 'WMK', 'MBTC', 'OJX', 'CHW', 'ABBC', 'CATT',
                   'VEX', 'LQDN', 'BIOC', 'FOREX', 'CPLO', 'XPX', 'RIPAX', 'HETA', 'NOW', 'ADAB', 'CIX100', 'FIH',
                   'MINX', 'MOBU', 'NVDX', 'COVEX', 'TAL', 'F2K', 'GTX', 'B21', 'LK', 'QOBI', 'BVO', 'VENA', 'CDRX',
                   'CRF', 'ELES', 'GEON', 'TZO', '433', 'WLME', 'INVX', 'AWT', 'ABXC', 'LINKC', 'BFC', 'IMPCN', 'XPT',
                   'FORK', 'NMK', 'OUT', 'LPT', 'RAINC ', 'IOVT', 'MYO', 'ORET', 'SEC', 'QUIZ', 'CYRS', 'UTL', 'JOYS',
                   'DACH', 'MNVM', 'PLTX', 'BTMG', 'BRIK', 'XTN', 'LUMA', 'BTZN', 'CLRTY', 'COING', 'NAVIB', 'ARTP',
                   'PLEO', 'GDX', 'EGDC', 'ENTT', 'RWD', 'AURUM', 'WRL', 'CRWD', 'ENCN', 'TAURI', 'EYE', 'GTR', 'HXC',
                   'OPEX', 'SKYM', 'SCIA', 'TXP', 'GPS', 'WTXH', 'BBG', 'NZE', 'FIELD', 'SHKG', 'TENZ', 'TWC', 'WUG',
                   'CAND', 'CTW', 'XIM', 'NAM', '2TF', 'BZKY', 'CARAT', 'ZILLA', 'TCJ', 'MAEP', 'DN8', 'XNT', 'PPOVR',
                   'LX', 'AWAX', 'VAR', 'TKD', 'VTAG', 'WBY', 'BBOS', 'BFEX', 'HUS', 'APXT', 'IDORU', 'WOM', 'BONA',
                   'HLDY', 'BLACK', 'HORUS', 'MEETONE', 'IOTW', 'EMPR', 'MPAY', 'AGM', 'MTCN', 'PTO', 'AS', 'OSF',
                   'DLPT', 'GREENT', 'VIDI', 'SIN', 'OPQ', 'ZYM', 'RPB', 'DYNCOIN', 'MIT', 'VANM', 'PSF', 'LITION',
                   'NEW', 'MZG', 'VIAZ', 'BTZC', 'ECR', 'RF', 'ARMS', 'MPXT', 'XELS', 'PGF7T', 'IDAC ', 'ZUUM',
                   'UCOINT', 'YDY', 'FTUM', 'SPON', 'DLXV', 'OCEANT', 'TECO', 'GOALS', 'ETHIX', 'TTB', 'CHK', 'VLTX',
                   'PRPT', 'OASC', 'TREE', 'GDL', 'LNT', 'FTRC', 'HBX', 'LAO', 'GOVT', 'COGEN', 'DAILY', 'SREUR',
                   'MAZC', 'TGTC', 'NRG', 'PLNX', 'IPT', 'IGTT', 'SRXIO', 'GZB', 'GGP', 'IFUM', 'ATC', 'DOOH', 'IOUX',
                   'BQTX', 'NVOY', 'CYBR', 'LLG', 'LCR', 'SNPC', 'VTM', 'NRX', 'BCNA', 'BTSG', 'CINX', 'CCIN', 'CCI',
                   'RDS', 'GMS', 'SGAT', 'SILKT', 'BITM', 'TCHN', 'FIII', 'ICHN', 'LVX', 'AENT', 'LYFE', 'REMCO',
                   'SaTT', 'GEMA', 'SCH', 'VTEX', 'SRV', 'DSLA', 'SYLO', 'YMZ', 'AER', 'AIBB', 'ASQT', 'AXC', 'BLKD',
                   'CYS', 'ATTR', 'CTY', 'DDL', 'COY', 'FNL', 'B2G', 'CSQ', 'HBE', 'ICT', 'TOS', 'CPROP', 'MOOLYA',
                   'PON', 'CREV', 'VAD', 'IDC', 'LBR', 'EMX', 'XBASE', 'LEN', 'KUBO', 'FABA', 'LQ8', 'GC', 'INFLR',
                   'LIB', 'PERMIAN', 'PETL', 'XDMC', 'PPS', 'SMILO', 'BCVB', 'TREX', 'VNS', 'VRF', 'AUX', 'LYQD', 'CBP',
                   'SMOKE', 'EDN', 'AVALA', 'NOS', 'DT1', 'FARMA', 'STACS', 'JMC', 'FOAM', 'FRED', 'CNCT', 'ENGT',
                   'VRTY', 'TEAMT', 'ZND', '3XD', 'FPC', 'SYNCO', 'SPY', '77G', 'HIDU', 'USE', 'NGIN', 'KOTO', 'GENX',
                   'XSC', 'VTL', 'SECI', 'SPRTZ', 'C25', 'LYN', 'STASH', 'HERB', 'AQUA', 'XQR', 'URX', 'KSYS', 'MTEL',
                   'MTT', 'MITC', 'BBTC', 'UMO', 'LIT', 'MUST', 'ELT', 'XNB', 'RBTC', 'BTCEX', 'PIRATE', 'EXO', 'ONAM',
                   'BIH', 'KARMA', 'CJR', 'BLTG', 'AGVC', 'ASGC', 'MIMI', 'PXG', 'ORM', 'TRET', 'SET', 'BEER', 'AERGO',
                   'TIMI', 'NRP', 'CEN', 'GARD', 'UNX', 'OWC', 'WOWX', 'SRX', 'THO', 'TOSS', 'KMX', 'SKI', 'SG',
                   'SUNEX', 'VIDY', 'XRBT', 'ALUX', 'XBOND', 'BOSE', 'JOY', 'WETH', 'GBE', 'HRBE', 'BEAM', 'MILC',
                   'PINMO', 'POPC', 'RGT', 'SCOP', 'BMG', 'OXY2', 'VC', 'FAIRC', 'BPN', 'DYC', 'LN', 'FTR', 'RWE',
                   'YSH', 'TASH', 'TXM', 'TRAVEL', 'ACA', 'AAT', 'AUPC', 'COSX', 'DNTX', 'HART', 'KSS', 'LIPS', 'MIBO',
                   'BRIX', 'NZO', 'PTT', 'XRK', 'RMOB', 'XRF', 'POD', 'SUT', 'WHO', 'ID', 'VRX Token', 'WDX', 'AIOT',
                   'AMOS', 'ESW', 'XBANK', 'OX', 'KRO', 'CAID', 'GUAR', 'LTE', 'MEL', 'NEXXO', 'QNTR', 'BTCUS', 'RAYS',
                   'MOL', 'REME', 'RENC', 'TLT', 'EMOT', 'USAT', 'VOLAIR', 'AIRT', 'VTRD', 'BTT', 'GALI', 'PLAI', 'BGG',
                   'HEDG', 'WBTC', 'ERE', 'BTU', 'APS', 'XBX', 'QNT', 'FFUEL', 'NSP', 'SNcoin', 'TTNT', 'FLC', 'BWT2',
                   'OATH', 'SBA', 'DXG', 'EXTP', 'ZEX', 'XCZ', 'CBUK', 'HIX', 'TGN', 'COGS', 'XRM', 'CCOIN', 'APZ',
                   'ICHX', 'IMP', 'FORCE', 'BTMX', 'QUSD', 'BTH', 'PLG', 'PVP', 'EMANATE', 'RAIZER', 'CP', 'DAYTA',
                   'ORV', 'CWT', 'AQU', 'CXG', 'CHFT', 'VNTY', 'MAI', 'BTR', 'SSX', 'KLK', 'LVN', 'FFCT', 'AZU', 'ARQ',
                   'WU', 'ZUC', 'FFM', 'DRF', 'GTIB', 'CR', 'VEO', 'DLA', 'AFO', 'BB1', 'FET', 'DAGT', 'GVE', 'IDT',
                   'KUV', 'YACHTCO', 'BOLTT', 'ENCX', 'VALID', 'TYM', 'VENUS', 'HYGH', 'ALCE', 'NODIS', 'MNC', 'USDS',
                   'HVE', 'XR', 'VALOR', 'ALP', 'EMU', 'GST', 'ARTC', 'NRM', 'APOD', 'AX', 'CWEX', 'CLDX', 'ECTE',
                   'LABX', 'ENV', 'ANKR', 'GEP', 'IZA', 'GBA', 'ITU', 'FANZ', 'CSPN', 'CCH', 'HAVEN', 'XOV', 'EQUAD',
                   'CURA', 'CREDIT', 'ERA', 'MAKE', 'SPKZ', 'AWC', 'DIS', 'SCRIBE', 'INXM', 'SQR', 'GNC', 'WVR', 'PHT',
                   'WHN', 'CRO', 'LYTX', 'TJA', 'InBit', 'DIO', 'LIC', 'SCA', 'XOS', 'VSYS', 'UGT', 'ZEON', 'XRX',
                   'PARQ', 'T4M', 'TFF', 'IZZY', 'SONT', 'SWI', 'LUNES', 'EDEXA', 'PPI', 'ANTE', 'TRXDICE', 'AFTT',
                   'TRXWIN', 'IGG', 'MIG', 'BWN', 'IPUX', 'PCC', 'DARB', 'MBTX', 'CFun', 'SLC', 'AAS', '2GT', 'VOLLAR',
                   'DXN', 'BUYI', 'AFCT', 'REDI', 'INET', 'WHY', 'URIS', 'ADUX', 'HRD', 'QCO', 'SHER', 'ZEROB', 'ISG',
                   'GEC', 'TAGZ', 'SKP', 'MCRC', 'XGN', 'YPTO', 'UBE', 'ETGP', 'GFCS', 'RDT', 'IX', 'ALIC', 'HCXP',
                   'AGRO', 'TFUEL', 'BYTS', 'GRT', 'EUCX', 'MYTV', 'LEVL', 'PNP', 'PRY', 'MXM', 'TTC', 'BCNX', 'EVED',
                   'HTER', 'GESE', 'BZRX', 'YBK', 'GIF', '2KEY', 'STG', 'DEVX', 'TMB', 'HBRS', 'XPL', 'MTSH', 'DAGO',
                   'TEMPO', 'PPR', 'REW', 'ORBS', 'STE', 'TPLAY', 'TELE', 'GYM', 'UDOO', 'KICKS', 'SPORTG', 'CRES',
                   'AES', 'AIBK', 'NCC', 'STONE', 'OILD', 'VLM', 'LOLC', 'CTLX', 'CSM', 'LOTES', 'LOTEU', 'RVO', 'GTH',
                   'KBT', 'USDX', 'LHT', 'PLAT', 'NYCREC', 'NSD', 'SOLVE', 'BOLT', 'BLOC', 'SPT', 'FBB', 'TCST',
                   'BSAFE', 'DBTN', 'HET', 'DARC', 'CMA', 'MAPR', 'THR', 'MATIC', 'PBET', 'SST', 'PUX', 'YANU', 'XCB',
                   'RSF', 'WMD', 'TOYKEN', 'XAL', 'TAS', 'UNTD', 'COVA', 'LAMB', 'FXC', 'GEX', 'VDL', 'TMN', 'TCR',
                   'FUNX', 'ASST', 'BEET', 'IFX', 'MART', 'TC', 'DAPPT', 'TTN', 'GNTO', 'OCEAN', 'LMXC', 'UTPL', 'GDR',
                   'LNX', 'ORIGIN', 'NTO', 'TXT', 'ARRR', 'SCONE', 'OWN', 'VLS', 'AWR', 'QQQ', 'ULED', 'UVU', 'KOZ',
                   'SMAT', 'IOWN', 'QBIT', 'BCX', 'LEO', 'BST', 'AYA', 'BUSDC', 'VCN', 'BAC', 'BLAST', 'PRDX', 'ZOPT',
                   'FILM', 'LUT', 'VDX', 'PHB', 'RSR', 'ONE', 'CKUSD', 'CTPT', 'ESBC', 'GRAYLL', 'BRC', 'MOC', 'SERV',
                   'PTON', 'DPN', 'VBK', 'THEMIS', 'YCC', 'USDK', 'MIX', 'PLY', 'BWX', 'VST', 'WIB', 'BOXX', 'UT', 'BU',
                   'DX', 'MTV', 'TRIAS', 'WINT', 'VNT', 'OGO', 'DVT', 'BOMB', 'CARRY', 'BRYLL', 'WXT', 'BOXT', 'KAT',
                   'BEST', 'CAM', 'HYDRO', 'BITNEW', 'ATP', 'BCV', 'BKN', 'INB', 'WICC', 'EKT', 'BIHU', '1SG', 'KT',
                   'INE', 'ARTF', 'AT', 'DEX', 'ELD', 'UOS', 'UND', 'PEOS', 'BHD', 'GTN', 'VIPS', 'BBGC', 'LINA',
                   'INFC', 'BTNT', 'WGP', 'NPXSXEM', 'YOU', 'USCC', 'ANDC', 'WGC', 'GMB', 'MRS', 'FUND', 'OCC', 'NNB',
                   'USDQ', 'ULT', 'WWB', 'VANT', 'SNET', 'IRIS', 'BTCB', 'IONC', 'SMARTS', 'CNUS', 'ABL', 'SDA',
                   'SMARTUP', 'HYN', 'UIP', 'MIR', 'JCT', 'FTI', 'DOS', 'LIBRA', 'DLO', 'DUOT', 'OCE', 'ALGO', 'AIRX',
                   'RAVEN', 'MIN', 'MBL', 'B91', 'AIDT', 'ALI', 'CLB', 'CZR', 'DELTA', 'GSE', 'KNT', 'KWATT', 'MAS',
                   'UCH', 'VDG', 'YEED', 'PRS', 'EHRT', 'XRC', 'TERA', 'MXC', 'JAR', 'VOCO', 'TNS', 'NBOT', 'RATING',
                   'AMPL', 'SOP', 'LEMO', 'TYPE', 'CYL', 'HLT', 'E2C', 'TAC', 'TENX', 'EKG', 'SLV', 'ERD', 'PHV',
                   'ONOT', 'IMPT', 'BITRUE', 'SWAPS', 'GNY', 'SRK', 'ACDC', 'YEC', 'TOKO', 'ECO', 'ADN', 'FTN', 'GRN',
                   'NTY', 'TEMCO', 'ADRX', 'MESG', 'SHX', 'UPX', 'FST', 'BCT', 'TRTT', 'THCH', 'ABX', 'HXRO', 'MONT',
                   'WIN', 'NUT', 'TN', 'PBQ', 'ZDR', 'DOCT', 'DTEP', 'TCHAIN', 'XRTC', 'VRSC', 'LUNA', 'VOL', 'BSOV',
                   'FTT', 'NAT', 'TRV', 'RET', 'GMAT', 'HUM', 'LOL', 'BCAC', 'XD', 'OTO', 'BQQQ', 'SIX', 'LOCUS',
                   'COZP', 'OGOD', 'SERO', 'FOIN', 'FKX', 'YTA', 'LXT', 'IMG', 'SXP', 'BOTX', 'DPT', 'GT', 'TRAT',
                   'CHZ', 'OPNN', 'SINS', 'BDX', 'DXR', 'PC', 'BUT', 'GOS', 'DEFI', 'BXK', 'KNOW', 'WFX', 'XPC', 'ACD',
                   'AKRO', 'AMON', 'BENZI', 'BGBP', 'BHP', 'XCHF', 'BXA', 'CBNT', 'DEEP', 'DOC', 'DTC', 'DVP', 'DWC',
                   'ELAC', 'ETSC', 'FMEX', 'FTK', 'FLEX', 'GE', 'GOT', 'INFT', 'ITOC', 'JCB', 'KSC', 'LHD', 'LKN',
                   'LPK', 'MMT', 'OSC', 'PIB', 'PNK', 'PROM', 'PROT', 'QQBC', 'SPIN', 'TCNX', 'THX', 'THEX', 'TCHTRX',
                   'UAT', 'UENC', 'ULTRA', 'URAC', 'USDSB', 'VINCI', 'WLO', 'XENO', 'XND', 'XSR', 'ZAIF', 'ETM', 'AMIO',
                   'FAB', 'VD', 'NYE', 'LTK', 'STREAM', 'BPRO', 'TOL', 'CVCC', 'EVT', 'NTBC', 'MEX', 'ATN', 'NASH',
                   'CUST', 'QCH', 'FO', 'SON', 'BKBT', 'BQT', 'BLOCM', 'WSD', 'SDS', 'ZT', 'GOM', 'BAND', 'OF', 'CBM',
                   'EMRX', 'HBAR', 'IZI', 'UC', 'TOSC', 'OVC', 'WIKEN', 'MCC', 'HVNT', 'PAXG', 'MEXC', 'NSS', 'TRP',
                   'MB', 'CENT', 'MB8', 'HSN', 'IDRT', 'ZUM', 'PIPL', 'BNANA', 'VNDC', 'MX', 'HUSD', 'GAP', 'DDAM',
                   'PLAC', 'MOGU', 'CXCELL', 'BGONE', 'TLOS', 'FLAS', 'DEQ', 'BCB', 'LBK', 'GSTT', 'ME', 'DMS', 'TREEC',
                   'SCTK', 'RON', 'SINX', 'HAZ', 'AIPE', 'MISS', 'DKKT', 'BTY', 'CSAC', 'TEM', 'BSTX', 'KAVA', 'DMC',
                   'CKB', 'KISC', 'VBT', 'G50', 'SEOS', 'ODC', 'GALT', 'LTBTC', 'DAI', 'TENA', 'SPLA', 'UNICORN',
                   'EONC', 'PRCM', 'BFCH', 'LIGHT', 'CBFT', 'TRDS', 'ETHPLO', 'YAP', 'LKU', 'SUTER', 'FMCT', 'NODE',
                   'LINKA', 'ZVC', 'OROX', 'ACU', 'OLXA', 'WIX', 'BRZE', 'BCZERO', 'BTC2', 'ECOREAL', 'S4F', 'BIPX',
                   'BOK', 'TEP', 'TSR', 'RUNE', 'HNB', 'DILI', 'CAI', 'FLG', 'MCH', '7E', 'XTX', 'LOBS', 'MGX', 'DAD',
                   'EUM', 'SOVE', 'BCS', 'THP', 'TKC', 'LT', 'MSN', 'W1', 'OFBC', 'CB', 'TD', 'DRINK', 'SNL', 'EOSC',
                   'GLOS', 'SEA', 'CBE', 'KLAY', 'DZCC', 'TRCB', 'TROY', 'MPL', 'UIN', 'XFC', 'WOW', 'USDN', 'ROAD',
                   'BRZ', 'GKI', 'FBN', 'EVY', 'PTN', 'KSM', 'TDE', 'ECP', 'XBG', 'PP', 'CNTM', 'MINTME', 'SCAP', 'FN',
                   'DYNMT', 'MDM', 'CCA', 'DFP', 'QTCON', 'GTSE', 'API', 'RES', 'AMAL', 'BIUT', 'MLGC', 'PSC', 'XDC',
                   'ALN', 'DMTC', 'TRB', 'TFB', 'DAMO', 'XSPC', 'OXT', 'USDG', 'DGLD', 'MAP', 'LVIP', 'BOA', 'PLF',
                   'CHARS', 'TYT', 'NVL', 'CSAI', 'CUSDC', 'CBAT', 'CZRX', 'CREP', 'CETH', 'CDAI', 'CWBTC', 'FCQ',
                   'BTCK', 'DAVP', 'XTP', 'ZYN', 'OGN', 'EXM', 'CUT', 'VEN', 'LTBX', 'IPX', 'ZANO', 'HEX', 'CYBER',
                   'NRV', 'KOK', 'KSH', 'HTDF', 'EGG', 'KRT', 'N8V', 'EBK', 'PEG', 'ERK', 'BNP', 'TUDA', 'APM', 'BLTV',
                   'RRB', 'MESH', 'WIKI', 'HINT', 'PCI', 'BNA', 'AXL', 'GOD', 'ALY', 'CODY', 'SPOK', 'USDH', 'KDA',
                   'GARK', 'IDHUB', 'IOEX', 'LM', 'BIKI', 'DLX', 'DALI', 'FLDT', 'TCO', 'ETY', 'LBXC', 'JOB', 'VEIL',
                   'BTBL', 'MKEY', 'TAUC', 'GIB', 'SCDS', 'CCX', 'SYM', 'ECT', 'GIX', 'SENNO', 'BEP', 'GANA', 'KAL',
                   'NEWOS', 'FNK', 'TSF', 'AIDUS', 'STEEP', 'ZOC', 'YTN', 'SCRIV', 'AREPA', 'CHEESE', 'PEPS', 'NEET',
                   'OMEGA', 'BBS', 'BZL', 'CRP', 'GSR', 'VARIUS', 'AGET', 'WRX', 'ZCR', 'AEVO', 'NAH', 'EGEM', 'DXO',
                   'GOSS', 'NYEX', 'GIO', 'TELOS', 'SIERRA', 'VIVID', 'RPD', 'PENG', 'MERI', 'KTS', 'NOR', 'BTCV',
                   'X42', 'XWP', 'CSNP', 'CALL', 'MOCO', 'WBET', 'ARMR', 'XSD', 'DIVO', 'WCC', 'HUSL', 'WLF', 'CNB',
                   'CTAG', 'CWN', 'HNS', 'BLINK', 'JUL', 'VEGA', 'BC', 'NCOV', 'ES', 'EER', 'USDA', 'BCZ', 'DBY', 'KAM',
                   'EBASE', 'SWYFTT', 'DOGZ', 'WPX', 'POCC', 'GFUN', 'NWC', 'CVA', 'JMT', 'XAUT', 'URBC', 'ABA', 'DSC',
                   'NAX', 'DAPP', 'XNC', 'AMDC', 'NNC', 'CCTN', 'TWEE', 'KBOT', 'EOSBULL', 'XRPBEAR', 'EUSD', 'ALLBI',
                   'ETR', 'FK', 'XLA', 'SOLO', 'ERG', 'BIRD', 'TCC', 'AUNIT', 'BNBBULL', 'BNBBEAR', 'ODX', 'TRYB',
                   'GLS', 'INS', 'TRXBULL', 'TRXBEAR', 'LTCBULL', 'LTCBEAR', 'AAB', 'BKRW', 'HBD', 'FRSP', 'ELAMA',
                   'ANCT', 'USDJ', 'QC', 'ALV', 'GZE', 'DACS', 'NII', 'UPEUR', 'UPUSD', 'UPT', 'CIM', 'EWT', 'MORE',
                   'HDAO', 'EURT', 'LCX', 'HIVE', 'THX!', 'COSP', 'HOTT', 'MZK', 'QUROZ', 'HUNT', 'VNXLU', 'AIN',
                   'PORTAL', 'IIC', 'BTCHG', '300F', 'HKDX', 'CNYX', 'NZDX', 'CHFX', 'CADX', 'USDEX', 'JPYX', 'AUDX',
                   'GOLDX', 'ZARX', 'TRYX', 'SGDX', 'RUBX', 'POLNX', 'SOLAN', 'EXCHBEAR', 'ALTBULL', 'EXCHBULL',
                   'ALTBEAR', 'BCHC', 'ZLS', 'PGX', 'SLVX', 'DEP', 'CTT', 'KDG', 'HMR', 'KIM', 'LMCH', 'SNB', 'CBUCKS',
                   'LAR', 'EUCOIN', 'QBZ', 'BSVBULL', 'BSVBEAR', 'FF1', 'BCHBULL', 'BCHBEAR', 'ISIKC', 'ZFL', 'PCX',
                   'CTSI', 'MWC', 'IQC', 'IDNA', 'IZER', 'XXA', 'SENSO', 'STAKE', 'IBVOL', 'BVOL', 'SATX', 'OBSR',
                   'UFOC', 'BONO', 'WADS', 'ALA', 'XTZBULL', 'XTZBEAR', 'EC', 'BTCT', 'NEWS', 'RHP', 'BTCSHORT', 'DUC',
                   'CNRG', 'JST', 'ADAI', 'ZNZ', 'NYZO', 'ICH', 'GLEEC', 'LRG', 'RVX', 'TNCC', 'ANJ', 'WET', 'ETHBN',
                   'PXP', 'L2L', 'YOUC', 'CWR', 'IBS', 'ZTN', 'DGN', 'QI', 'TRNSC', 'GLDS', 'CTE', 'LLION', 'SOW',
                   'PWON', 'Si14', 'NCR', 'SKFT', 'NMT', 'TUNEZ', 'TOX', 'SONA', 'BRAND', 'NTS', 'WSLT', 'ENC', 'SETI',
                   'SDAT', 'IGCH', 'BNS', 'PXB', 'LUM', 'TYC', 'JUP', 'JACS', 'RWN', 'SETS', 'WRZ', 'ITAM', 'WOONK',
                   'ESH', 'MDNA', 'CPI', 'JUI', 'TWT', 'MNRL', 'METAC', '1GOLD', 'LOON', 'CGLD', 'NDN', 'GGC', 'BIZZ',
                   'XIO', '1UP', 'AFFC', 'BAN', 'BBDT', 'CDL', 'GLDY', 'CNHT', '1211.CUR', '1810.CUR', '9988.CUR',
                   'TERADYNE', 'SESG.CUR', 'TRIPAD', 'AAPL.CUR', 'PNC.CUR', 'EXAS.CUR', 'IPN.CUR', 'STM.CUR',
                   'TSLA.CUR', 'SDC.CUR', 'JBL.CUR', 'WLL.CUR', 'Oil - Crude.CUR', 'BILL.CUR', 'BBY.CUR', 'BILI.CUR',
                   'GME.CUR', 'AA.CUR', 'BSX.CUR', 'TFX.CUR', 'NKE.CUR', 'ABBV.CUR', 'AN.CUR', 'AAP.CUR', 'AR.CUR',
                   'RH.CUR', 'JCP.CUR', 'EPAM.CUR', 'ATVI.CUR', 'WMT.CUR', 'BA.CUR', 'TGT.CUR', 'YNDX.CUR', 'ROKU.CUR',
                   'CVS.CUR', 'C.CUR', 'LHA.CUR', 'BLUE.CUR', 'F.CUR', 'DDOG.CUR', 'K.CUR', 'M.CUR', 'SOHU.CUR',
                   'DHR.CUR', 'TXT.CUR', 'SLCA.CUR', 'R.CUR', 'BYND.CUR', 'S.CUR', 'IBM.CUR', 'XPO.CUR', 'V.CUR',
                   'W.CUR', 'X.CUR', 'VI', 'MXW', 'SDT', 'FORESTPLUS', 'DDK', 'MTXLT', 'LQBTC', 'XPR', 'UTI',
                   'CN50.CUR', 'SQ.CUR', 'CC.CUR', 'NVDA.CUR', 'NZD.CUR', 'TWTR.CUR', 'MTCH.CUR', 'FTXR.CUR',
                   'FR40.CUR', 'SWN.CUR', 'DIS.CUR', 'INTC.CUR', 'INCY.CUR', 'TEAM.CUR', 'AMZN.CUR', 'DWDP.CUR',
                   'ALXN.CUR', 'AUD.CUR', 'DE30.CUR', 'DE.CUR', 'DG.CUR', 'SRPT.CUR', 'APAM.CUR', 'CHK.CUR', 'KHC.CUR',
                   'BBBY.CUR', 'GPS.CUR', 'ADS.CUR', 'CRON.CUR', 'FIVE.CUR', 'PBF.CUR', 'TLRY.CUR', 'GRUB.CUR',
                   'PAYC.CUR', 'DLPH.CUR', 'BABA.CUR', 'JWN.CUR', 'PBR.CUR', 'GOLD.CUR', 'CHF.CUR', 'NL25.CUR',
                   'EMN.CUR', 'HCA.CUR', 'PBYI.CUR', 'AEM.CUR', 'SIG.CUR', 'Silver.CUR', 'SYY.CUR', 'NOW.CUR',
                   'VOO.CUR', 'EXEL.CUR', 'ICPT.CUR', 'FB.CUR', 'QRVO.CUR', 'OAS.CUR', 'CSCO.CUR', 'IT40.CUR',
                   'PTON.CUR', 'GPRO.CUR', 'GWPH.CUR', 'FP.CUR', 'MNK.CUR', 'WB.CUR', 'NTES.CUR', 'MSFT.CUR',
                   'SHOP.CUR', 'WBA.CUR', 'LLY.CUR', 'IFX.CUR', 'GD.CUR', 'GE.CUR', 'NKTR.CUR', 'MOMO.CUR', 'BIG.CUR',
                   'ONEM.CUR', 'WATT.CUR', 'ALLY.CUR', 'AGN.CUR', 'SWKS.CUR', 'CAD.CUR', 'AFp.CUR', 'GT.CUR', 'AZBI',
                   'DVX', 'AR', 'ASM', 'GHOST', 'TFT', 'HIBS', 'BZUN.CUR', 'TMUS.CUR', 'XEC.CUR', 'CLVS.CUR', 'PEP.CUR',
                   'TEVA.CUR', 'ISRG.CUR', 'BIDU.CUR', 'PFE.CUR', '522.CUR', 'COMM.CUR', 'SBUX.CUR', 'IRBT.CUR',
                   'SBER.CUR', 'VOW3.CUR', 'YY.CUR', 'OGZD.CUR', 'DLTR.CUR', 'IP.CUR', 'ALNY.CUR', 'AIR.CUR', 'SMG.CUR',
                   'MAC.CUR', 'YOLO.CUR', 'FVRR.CUR', 'FSLR.CUR', 'JKS.CUR', 'DKA', 'RNX', 'KDAG', 'KVI', 'DRM',
                   'PAXGBULL', 'PAXGBEAR', 'PAXGHALF', 'PHNX', 'MHLX', 'SPICE', 'GGOLD', 'ALCH', 'SODA', 'GILD.CUR',
                   'RAD.CUR', 'APA.CUR', 'MGM.CUR', 'GRMN.CUR', 'UAA.CUR', 'ADNT.CUR', 'LYFT.CUR', 'WORK.CUR',
                   'MCHP.CUR', 'MRVL.CUR', 'US500.CUR', 'MRK.CUR', 'NDA.CUR', 'SNE.CUR', 'CNX.CUR', 'VNET.CUR',
                   'WFC.CUR', 'QCOM.CUR', 'SP35.CUR', 'FDX.CUR', 'US30.CUR', 'TPX.CUR', 'NFLX.CUR', 'TWLO.CUR',
                   'KO.CUR', 'RMD.CUR', 'BTC3L', 'EU50.CUR', 'DAI.CUR', 'BTC3S', 'BMW.CUR', 'ETH3L', 'DAL.CUR',
                   'MCD.CUR', 'ETH3S', 'ADABEAR', 'ADABULL', 'MATICBULL', 'MATICBEAR', 'ATOMBULL', 'ATOMBEAR',
                   'ALGOBULL', 'ALGOBEAR', 'KNCBULL', 'THETABULL', 'KNCBEAR', 'BEARSHIT', 'ETCBULL', 'ETCBEAR',
                   'TOMOBEAR', 'TOMOBULL', 'DRGNBEAR', 'DRGNBULL', 'THETABEAR', 'MIDBEAR', 'MIDBULL', 'OKBBEAR',
                   'OKBBULL', 'BTMXBEAR', 'BTMXBULL', 'LEOBULL', 'LEOBEAR', 'HTBEAR', 'HTBULL', 'DOGEBULL', 'DOGEBEAR',
                   'PRIVBEAR', 'PRIVBULL', 'USDTBULL', 'USDTBEAR', 'WDAY.CUR', 'SNAP.CUR', '241.CUR', 'HMI.CUR',
                   'XLV.CUR', 'PYPL.CUR', 'SSA.CUR', 'UBER.CUR', 'VLDY', 'NEE.CUR', 'CPRT.CUR', 'CPB.CUR', 'LB.CUR',
                   'NEM.CUR', 'ADPT.CUR', 'ETL.CUR', 'NET.CUR', 'OSTK.CUR', 'AMUN.CUR', 'BMRN.CUR', 'Platinum.CUR',
                   'TTWO.CUR', 'NCLH.CUR', 'GOOGL.CUR', 'BNTX.CUR', 'EDF.CUR', 'CBK.CUR', 'OCFT.CUR', 'EXPE.CUR',
                   'JNJ.CUR', 'JPM.CUR', 'VGT.CUR', 'BIIB.CUR', 'PTEN.CUR', 'STLD.CUR', 'TRI.CUR', 'GLPG.CUR',
                   'YELP.CUR', 'ARNC.CUR', 'ADBE.CUR', 'SAGE.CUR', 'LKOD.CUR', 'EBAY.CUR', 'DBK.CUR', 'Palladium.CUR',
                   'ORCL.CUR', 'LX.CUR', 'CAG.CUR', '1COV.CUR', 'MU.CUR', 'SPN.CUR', 'CTLT.CUR', 'CIEN.CUR', 'MJ.CUR',
                   'DBX.CUR', 'AMD.CUR', 'XLNX.CUR', 'MC.CUR', 'MA.CUR', 'RNO.CUR', 'FTCH.CUR', 'OHL.CUR', 'TER.CUR',
                   'TRIP.CUR', 'COMP', 'CGT', 'UMA', 'CUSDT', 'BTRS', 'CELO', 'D4RK', 'BTCUP', 'BTCDOWN', 'BIDR', 'BAL',
                   'DAWN', 'IDK', 'BTSE', 'PAMP', 'CODEO', 'DOT', 'MP', 'DMG', 'BTE', 'LUCY', 'POL', 'ARX', 'PMGT',
                   'PAZZI', 'PQT', 'ISP', 'SILKR', 'CCOMM', 'LACCOIN', 'KAI', 'BASIC', 'VARC', 'CRD', 'TRCL', 'EFK',
                   'INNOU', 'CVS', 'ZLST', 'JUR', 'OZP', 'SAC1', 'SCP', 'SWAP', 'KEEP', 'BKS', 'CCXX', 'BPS', 'RAKU',
                   'DMCH', 'PLAAS', 'NEAL', 'AMA', 'VEDX', 'WEST', 'BRTR', 'UFC', 'TTM', 'ETHUP', 'ETHDOWN', 'LINKDOWN',
                   'LINKUP', 'ADADOWN', 'ADAUP', 'IDX', 'FXF', 'OKS', 'XANK', 'FIO', 'BLX', 'DEXT', 'FOUR', 'XGM',
                   'ALEPH', 'STONK', 'NEXBT', 'MTA', 'DFI', 'YFI', 'SWINGBY', 'DECENTR', 'ECOCH', 'PROB', 'VXV', 'XOR',
                   'HNT', 'PLT', 'DEMOS', 'NEST', 'HYBN', 'UHP', 'IMST', 'GEODB', 'UBU', 'DDRT', 'MCB', 'ATT', 'WNXM',
                   'HOMI', 'CNS', 'TEND', 'MDU', 'XAMP', 'FOCV', 'INRT', 'LIDER', 'KTON', 'SUKU', 'FEX', 'DIA', 'AOS',
                   'DF', 'BPLC', 'AICO', 'FLS', 'ETHP', 'MLK', 'LID', 'CREAM', 'GEEQ', 'STAMP', 'BULLC', 'DPIE', 'RMPL',
                   'XRT', 'MGP', 'JT', 'ZNN', 'SRM', 'NXM', 'EDGEW', 'ANW', 'CRV', 'BDCC', 'CORX', 'PAR', 'BREE',
                   'PERX', 'SAND', 'BNBUP', 'BNBDOWN', 'XTZUP', 'XTZDOWN', 'PRQ', 'BLY', 'RENBTC', 'ZZZ', '4ART',
                   'CAPT', 'YFII', 'TRUST', 'YFL', 'ANY', 'MXX', 'ETHV', 'REAP', 'BRDG', 'DZI', 'ZLW', 'BART', 'XIOT',
                   'PSG', 'HUP', 'SHB', 'RWS', 'ZIN', 'KLP', 'ZPAE', 'UNT', 'FSW', 'HAKKA', 'JRT', 'SUSHI', 'STOP',
                   'HTN', 'DGVC', 'PDF', 'RUG', 'CVPT', 'CATX', 'DFIO', 'NEWTON', 'VIDYA', 'QQQF', 'LIBFX', 'LIEN',
                   'FME', '$BASED', 'YFFI', 'KLV', 'LYRA', 'STATERA', 'PEARL', 'TAI', 'EGLD', 'DEXG', 'YFIS', 'CHAIN',
                   'OIN', 'SLINK', 'TOMA', 'UNIFI', 'DACC2', 'SOFI', 'YFIVE', 'BAST', 'YFIE', 'RELVT', 'OPTC', 'INXP',
                   'HAI', 'UST', 'TLN', 'KARMAD', 'CORN', 'SALMON', 'JFI', 'QOOB', 'BEL', 'MATH', 'MEDICO', 'SEEDV',
                   'BTCAS', 'LGOT', 'CELOUSD', 'XFTC', 'SUN', 'SWRV', 'EOSUP', 'EOSDOWN', 'TRXUP', 'TRXDOWN', 'XRPUP',
                   'XRPDOWN', 'DOTUP', 'DOTDOWN', 'POWER', 'AMP', 'UMI', 'HGET', 'LTCUP', 'LTCDOWN', 'RVC', 'PHA',
                   'CRT', 'BOT', 'YSAFE', 'UNIFUND', 'UTOPIA', 'TYS', 'ACH', 'XT', 'WING', 'SASHIMI', 'UNDB', 'SAKE',
                   'YFFC', 'ZDEX', 'DPI', 'YFARM', 'CHADS', 'KATANA', 'ANK', 'CNYT', 'REVV', 'UNI', 'ZYRO', 'PRINT',
                   'HBC', 'WNRZ', 'PFID', 'DBOX', 'VYBE', 'NUTS', 'TRBT', 'SUSHIBULL', 'SUSHIBEAR', 'UNISWAPBULL',
                   'UNISWAPBEAR', 'XETH', 'YFFII', 'ETHPY', 'JIAOZI', 'ON', 'XSTAR', 'ASK', 'SOCKS', 'RARI', 'EVCC',
                   'RTH', 'ARDX', 'NSBT', 'DOGEC', 'QAC', 'HTA', 'CR8', 'DIC', 'BAK', 'DVS', 'CRDT', 'BCEO', 'BITC',
                   'LOT', 'BXC', 'DSCP', 'SURE', 'RC20', 'TOC', 'NBS', 'SCFIV2', 'GSTC', 'CHVF', 'GALA', 'LGCY', 'UCO',
                   'RIO', 'DHT', 'CHI', 'SHROOM', 'YSR', 'FLOW', 'KASSIAHOME', 'DAB', 'YFF', 'MEXP', 'DTOP', 'GPKR',
                   'MFC', 'SPRKL', 'SBE', 'STS', 'FLM', 'YFBETA', 'LMY', 'DCASH', 'PTF', 'INX', 'TONT', 'AVAXIOU',
                   'MARO', '$ROPE', 'VELO', 'BURGER', 'BAKE', 'MINI', 'EMN', 'ONIT', 'TITAN', 'AGS', 'CRU', 'POLS',
                   'WBNB', 'LUA', 'AETH', 'ISDT', 'CAKE', 'BASID', 'BWF', 'YFBT', 'FAME', 'MXT', 'FFYI', 'UFFYI', 'FAG',
                   'NIN', 'DMD', 'AHT', 'SFG', 'PJM', 'UNII', 'AAVE', 'PGT', 'EPIC', 'XVS', 'XFI', 'CORE', 'BID',
                   'KING', 'DAOVC', 'HOTN', 'SCRT', 'IOV', 'HLPT', 'DICETRX', 'BEC', 'WISE', 'AXEL', 'TOMOE', 'KOMP',
                   'DODO', 'FIT', 'BRG', 'EPS', 'CVP', 'BBC', 'XSP', 'TRIX', 'YFIII', 'PLAYD', 'BUY', 'ECELL', 'UNIUP',
                   'UNIDOWN', 'KIF', 'DUN', 'UCA', 'NEAR', 'WBX', 'DDR', 'CUTE', 'SYBC', 'PLTC', 'USG', 'SEAL', 'OCTO',
                   'MBN', 'BTTR', 'OWL', 'EASY', 'DEXE', 'STBZ', 'ZEFU', 'SXPUP', 'SXPDOWN', 'YUSRA', 'SPC', 'POST',
                   'CUR', 'ASTA', 'NU', 'FILUP', 'FILDOWN', 'YFIUP', 'YFIDOWN', 'HLX', 'UFT', 'AKT', 'ZEE', 'NICE',
                   'UBXT', 'LCG', 'SWAG', 'UNCX', 'HTHEDGE', 'HTHALF', 'HEDGESHIT', 'HALFSHIT', 'HALF', 'EXCHHEDGE',
                   'EXCHHALF', 'ETHHEDGE', 'ETHHALF', 'ETCHEDGE', 'ETCHALF', 'EOSHEDGE', 'EOSHALF', 'DRGNHEDGE',
                   'DRGNHALF', 'DOGEHEDGE', 'DOGEHALF', 'DMGBULL', 'DMGBEAR', 'DEFIHEDGE', 'DEFIHALF', 'DEFIBULL',
                   'DEFIBEAR', 'CUSDTHEDGE', 'CUSDTHALF', 'CUSDTBULL', 'CUSDTBEAR', 'COMPHEDGE', 'COMPHALF', 'COMPBULL',
                   'COMPBEAR', 'BULLSHIT', 'BTMXHEDGE', 'BTMXHALF', 'BSVHEDGE', 'BSVHALF', 'BNBHEDGE', 'BNBHALF',
                   'BCHHEDGE', 'BCHHALF', 'BALHEDGE', 'BALHALF', 'BALBULL', 'BALBEAR', 'ATOMHEDGE', 'ATOMHALF',
                   'ALTHEDGE', 'ALTHALF', 'ALGOHEDGE', 'ALGOHALF', 'ADAHEDGE', 'ADAHALF', 'SPEED', 'TRYBBULL',
                   'TRYBBEAR', 'TRXHEDGE', 'TRXHALF', 'TOMOHEDGE', 'TOMOHALF', 'TRYBHALF', 'THETAHEDGE', 'VETBEAR',
                   'SXPHEDGE', 'TRYBHEDGE', 'USDTHALF', 'SXPHALF', 'SXPBULL', 'SXPBEAR', 'PRIVHEDGE', 'PRIVHALF',
                   'PAXGHEDGE', 'OKBHEDGE', 'OKBHALF', 'MKRBULL', 'MKRBEAR', 'MIDHEDGE', 'MIDHALF', 'MATICHEDGE',
                   'MATICHALF', 'LTCHEDGE', 'LTCHALF', 'LINKHEDGE', 'LINKHALF', 'LEOHEDGE', 'LEOHALF', 'KNCHEDGE',
                   'KNCHALF', 'AFC', 'HMST', 'GRIN', 'ATOM', 'NLG', 'FTC', 'XZC', 'WAXP', 'NEBL', 'ZEN', 'GO', 'ELA',
                   'DGB', 'NULS', 'DASH', 'ARK', 'OMG', 'HOLO', 'HMT', 'HP', 'AQT', 'HNY', 'CAMP', 'KOREC', 'KORE',
                   'RAMP', 'WINR', 'DRC', 'XTZHEDGE', 'XTZHALF', 'XRPHEDGE', 'XRPHALF', 'XAUTHEDGE', 'XAUTHALF',
                   'XAUTBULL', 'XAUTBEAR', 'VETHEDGE', 'VETBULL', 'PRIA', 'FARMC', 'FARM', 'DAM', 'BUX', 'AUDIO', 'XHT',
                   'RUC', 'AXIAV3', 'WON', 'BOR', 'USNBT', 'NBT', 'SSL', 'CTK', 'USDF', 'XLT', 'STPL', 'ENG', 'RING',
                   'NPXS', 'KP3R', 'SUSD', 'DREP', 'FUN', 'HPT', 'AGI', 'DAG', 'COCOS', 'MLN', 'QASH', 'VGX', 'STPT',
                   'CNNS', 'DAC', 'TOPN', 'NAS', 'BORA', 'FOR', 'BTCVT', 'CVC', 'IBP', 'VELOX', 'VLX', 'TBTC', 'RSV',
                   'PERP', 'BLCT', 'VALUE', 'YFV', 'DXD', 'YO', 'CONT', 'APIX', 'BULL', 'QSP', 'CTXC', 'RKN', 'KAN',
                   'ARPA', 'ROOBEE', 'STMX', 'BMX', 'MFT', 'SAI', 'MTL', 'RINGX', 'DENT', 'CCOMP', 'AG8', 'PEAK', 'WOO',
                   'SLP', 'COFIX', 'ECU', 'DUCATO', 'BCHUP', 'BCHDOWN', 'FIS', 'BSV', 'XIN', 'EMC2', 'UBQ', 'RDD',
                   'SIB', 'XDN', 'IOC', 'ETP', 'CLOAK', 'RVN', 'DOGE', 'BURST', 'SC', 'POA', 'GBYTE', 'STRAT', 'IOST',
                   'WAN', 'MIOTA', 'STEEM', 'BTS', 'WAVES', 'ADA', 'CNTR', 'FIN', 'RIF', 'IZE', 'ROSE', 'GUSD', 'LOOM',
                   'BHAO', 'SURF', 'PTERIA', 'LYXE', 'ERSDL', 'WEMIX', 'N0031', 'ETHBULL', 'BKK', 'CVNT', 'AAC', 'TSHP',
                   'KEY', 'OM', 'BIX', 'ABT', 'XDGB', 'MSDT', 'PPT', 'DEGO', 'GHST', 'TRADE', 'LET', 'YEE', 'FYZ',
                   'GTO', 'SUP8EME', 'CDN', 'HARD', 'ORAI', 'REP', 'KP4R', 'AUSCM', 'XPRT', 'XFYI', 'MOONDAY', 'FWT',
                   'HD', 'SPORE', 'CHR', '300', 'CELR', 'MVL', 'FRONT', 'PNT', 'DUSK', 'SNTVT', 'GOM2', 'PERL', 'MOF',
                   'RDNN', 'ELAD', 'FNB', 'MDA', 'CROAT', 'PAY', 'PRE', 'MITX', 'BEAR', 'PIXEL', 'MET', 'LBA', 'SMT',
                   'DOCK', 'GNX', 'UGAS', 'UPP', 'BFT', 'AXS', 'DFD', 'MSB', 'XAT', 'XDOT', 'BOOB', 'EOSDT', 'GBK',
                   'SEELE', 'TAT', 'GSWAP', 'YYFI', 'DFGL', 'NVA', 'LEX', 'BLOODY', 'ASP', 'PICKLE', 'CTCN', 'ETHBEAR',
                   'PRO', 'TNB', 'QUN', 'MTX', 'APPC', 'CMT', 'EOSBEAR', 'ITC', 'DMT', 'FAIRG', 'EM', 'EPT', 'WABI',
                   'BOX', 'SPENDC', 'TRUMPLOSE', 'EGT', 'SRN', 'XRPBULL', 'ABYSS', 'OST', 'RUFF', 'RFUEL', 'LINKBEAR',
                   'TCT', 'EVX', 'BEPRO', 'TEN', 'MVP', 'PVT', 'SYN', 'YSEC', 'SMPL', 'DOGDEFI', 'TKN', 'NEC', 'COTI',
                   'FRM', 'FSN', 'INJ', 'DVI', 'AREI', 'ATRI', 'BUSD', 'XPN', 'PST', '8X8', 'LTO', 'MEME', 'TRUMPWIN',
                   'GOF', 'CDT', 'XUC', 'FAT', 'LINKBULL', 'FLETA', 'OGSP', 'SPKL', 'SMARTCREDIT', 'JEM', 'TSLA',
                   'WCCX', 'NAMI', 'FTM', 'BNB', 'QRK', 'EXP', 'GUP', 'MEC', 'ETN', 'AUR', 'GAME', 'BCD', 'NMC', 'BTG',
                   'KIN', 'GRS', 'VIA', 'SYS', 'SMART', 'XWC', 'ACT', 'VIDT', 'XVG', 'SKY', 'HPB', 'BCN', 'AE', 'BLK',
                   'BTM', 'HC', 'MOAC', 'BLOCK', 'GXS', 'WTC', 'BCH', 'XAS', 'AION', 'SHIFT', 'NAV', 'ZIL', 'VET',
                   'QTUM', 'ZEC', 'VTC', 'XTZ', 'NANO', 'ONT', 'LSK', 'ETC', 'XEM', 'LTC', 'XMR', 'DCR', 'BTC', 'XLM',
                   'ETH', 'TRX', 'NEO', 'XRP', 'EOS', 'SNM', 'RFR', 'TRIO', 'BHT', 'SNX', 'TON', 'ORN', 'ADEL', 'YAM',
                   'LRC', 'LRN', 'WGRT', 'RFOX', 'ROT', 'NEX', 'LST', 'MTRG', 'PIVX', 'TT', 'AKN', 'FNCX', 'FNX',
                   'ALPHA', 'AVAX', 'YAMV1', 'YAMV2', 'META', 'LOKI', 'FIL', 'HOT', 'USDTHEDGE']

    if crypto in crypto_list:
        crypto_call = cryptocompare.get_price(str(crypto), curr='USD')
        for x, v in crypto_call.items():
            for c, b in v.items():
                return f'The current price of ${crypto} is {b}$ :moneybag:'
    elif crypto not in crypto_list:
        return f':no_entry_sign: CURRENCY NOT FOUND, TRY AGAIN :no_entry_sign:'


def poke_api(msg):
    """uses pokepy and pokeapi
    https://pokeapi.github.io/pokepy/"""
    try:
        pokemon_name = pokepy.V2Client().get_pokemon(msg)

        response = f'Name: {pokemon_name.name}\n' \
                   f'Weight: {pokemon_name.weight}\n' \
                   f'Type: {pokemon_name.types[0].type.name}'
        return response
    except:
        error_code = f'{msg} IS NOT A POKEMON'
        return error_code


def week_api():
    a = requests.get('http://ukenummer.no/json')
    p = json.loads(a.text)
    s = json.dumps(p, indent=2, sort_keys=True)

    for k, v in p.items():

        if k == 'weekno':
            weekno = str(v)
        if k == 'dates':
            return f'It is currently week {weekno}, which lasts from {str(v["fromdate"])} to {str(v["todate"])}.'


def covid_api():
    a = requests.get('https://api.covid19api.com/summary')
    p = json.loads(a.text)
    s = json.dumps(p)

    for k, v in p.items():
        loc = 'Global'
        if k == loc:
            stats = (f'Coronavirus Statistics for {loc}: \n' +
                     'Total Cases: ' + str(v['TotalConfirmed']) + '\n' +
                     'New Cases: ' + str(v['NewConfirmed']) + '\n' +
                     'Total Deaths: ' + str(v['TotalDeaths']) + '\n' +
                     'New Deaths: ' + str(v['NewDeaths']) + '\n' +
                     'Data Collected from https://covid19api.com/\n' + 'Stay Safe'
                     )
            return stats


# function for retrieving posts from reddit
def reddit_meme():
    s = random.choice(sub_list)
    sub = r.subreddit(s)

    for a in sub.hot(limit=20):
        random_post_number = random.randint(2, 25)
        for i, posts in enumerate(sub.hot(limit=20)):
            if i == random_post_number:
                return f'Title: **{posts.title}**\n' \
                       f'{posts.url} \n' \
                       f' {random.choice(list_of_stealing)} _/r/{sub}_'


def facts():
    URL = 'https://uselessfacts.jsph.pl/random.json?language=en'

    r = requests.get(URL).json()
    for key, value in r.items():
        if key == 'text':
            fact = f'{value}\n' \
                   f'Facts collected from https://uselessfacts.jsph.pl/ !'
            return fact


def delete_DL():
    while True:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
            print('Cleaned')
            time.sleep(900)


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': f'{folder}/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(source=filename, **ffmpeg_options), data=data)


class Finance(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command()
    async def crypto(self, ctx):
        content = ctx.message.content
        a = content.split(' ', 1)
        msg = a[1]
        u_msg = msg.upper()
        await ctx.send(crypto_price(u_msg))


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command(description='Test')
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=ffmpeg_ex,
                                                                     source=query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def sb(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=ffmpeg_ex,
                                                                     source=query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def text(self, ctx, *, query):
        """Text to speech, output in channel user is in"""
        tts = gTTS(text=query, lang='en')
        tts.save('tts.mp3')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=ffmpeg_ex,
                                                                     source='tts.mp3'))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def textjoke(self, ctx):
        """Uses pyjokes library to create a text to speech file, and plays in channel user is in"""
        joke = pyjokes.get_joke()

        tts = gTTS(text=joke, lang='en')
        tts.save('textjoke.mp3')
        query = 'textjoke.mp3'
        # CHANGE THE EXECUTABLE TO YOUR FFMPEG DIRECTORY
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=ffmpeg_ex,
                                                                     source=query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=ffmpeg_ex,
                                                                         source=player))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    @text.before_invoke
    @sb.before_invoke
    @textjoke.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Sends a random meme')
    async def meme(self, ctx):
        await ctx.send(reddit_meme())


class Funny(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command()
    async def pokemon(self, ctx):
        content = ctx.message.content
        a = content.split(' ', 1)
        msg = a[1]
        await ctx.send(poke_api(msg))

    @commands.command(description='Sends a random joke, uses PyJokes Library')
    async def joke(self, ctx):
        await ctx.send(pyjokes.get_joke())

    @commands.command(description='Helps you with all of lifes questions')
    async def guidance(self, ctx):
        await ctx.send(eight_answer())

    @commands.command(description='Who is up for a gamble?')
    async def gamble(self, ctx):
        await ctx.send('Alright everyone, place your bets! Pick a number between 1-10 and whoever gets it right wins')
        time.sleep(2)
        await ctx.send('8 seconds left!')
        time.sleep(2)
        await ctx.send('6 seconds left!')
        time.sleep(2)
        await ctx.send('4 seconds left!')
        time.sleep(2)
        await ctx.send('2 seconds left!')
        time.sleep(1)
        await ctx.send('1 seconds left!')
        time.sleep(1)
        await ctx.send(f'The correct number was {random.choice(range(1, 10))}')

    @commands.command(description='Displays a random fact!')
    async def facts(self, ctx):
        await ctx.send(facts())


class Dnd(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def d2(self, ctx):
        diceroll = random.randint(1, 2)
        await ctx.send(diceroll)

    @commands.command()
    async def d4(self, ctx):
        diceroll = random.randint(1, 4)
        await ctx.send(diceroll)

    @commands.command()
    async def d6(self, ctx):
        diceroll = random.randint(1, 6)
        await ctx.send(diceroll)

    @commands.command()
    async def d8(self, ctx):
        diceroll = random.randint(1, 8)
        await ctx.send(diceroll)

    @commands.command(aliases=['dndice 10'])
    async def d10(self, ctx):
        diceroll = random.randint(1, 10)
        await ctx.send(diceroll)

    @commands.command()
    async def d12(self, ctx):
        diceroll = random.randint(1, 12)
        await ctx.send(diceroll)

    @commands.command()
    async def d20(self, ctx):
        diceroll = random.randint(1, 20)
        await ctx.send(diceroll)


class Misc(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command()
    async def changelog(self, ctx):
        await ctx.send(CHANGELOG)

    @bot.command(description='Cleans the chat')
    @commands.has_permissions(administrator=True)
    async def clean(self, ctx, limit: int):
        """method for cleaning chat, only administrator can use this"""

        await ctx.message.channel.purge(limit=limit)
        await ctx.channel.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

    @clean.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send("You cant do that!")

    @commands.command()
    async def slap(self, ctx):
        """Slaps the specified user"""
        try:
            user = ctx.message.mentions[0]

            await ctx.send(f'{user.mention} HOWS IT FEEL GETTING SLAPPED\n '
                           f'https://tenor.com/view/amanda-bynes-slap-gif-4079563')
        except:
            author = ctx.message.author
            await ctx.send(f'{author.mention} YOU GOTTA DO !SLAP @USERNAME \n '
                           f'https://tenor.com/view/amanda-bynes-slap-gif-4079563')

    @commands.command()
    async def covid(self, ctx):
        await ctx.send(covid_api())

    @commands.command()
    async def week(self, ctx):
        await ctx.send(week_api())


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Your friendly neighbourhood Niklas')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('------')
    activity = discord.Game(name=f"!help, version {VERSION}")
    await bot.change_presence(status=discord.Status.online, activity=activity)


t1 = threading.Thread(target=delete_DL)
t1.start()

# if a new class for commands is created, it needs to be added here so it can be recognised
bot.add_cog(Dnd(bot))
bot.add_cog(Misc(bot))
bot.add_cog(Funny(bot))
bot.add_cog(Finance(bot))
bot.add_cog(Reddit(bot))
bot.add_cog(Music(bot))
bot.run(TOKEN)
