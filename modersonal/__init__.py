from datetime import datetime

__author__ = 'Tom M. Ragonneau'
__email__ = 'tom.ragonneau@connect.polyu.hk'
__date__ = datetime(2020, 8, 19)
if datetime.now().year == __date__.year:
    __copyright__ = 'Copyright {}, {}'.format(datetime.now().year, __author__)
else:
    __copyright__ = 'Copyright {}-{}, {}'.format(__date__.year, datetime.now().year, __author__)
__license__ = 'GNU General Public License (GPLv3)'
__version__ = '1.0.0'
__credits = [__author__]
__maintainer__ = __author__
__status__ = 'Development'
