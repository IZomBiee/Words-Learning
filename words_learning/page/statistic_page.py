from vocabulary import Statistic

from matplotlib import pyplot as plt


def statistic_page_loop():
    plt.title("All statistic of all time")
    plt.xlabel("Dates")
    plt.ylabel("Count")
    plt.plot([i['date'] for i in Statistic()], [round(float(i['time_in_learning'])/60, 2) for i in Statistic()], marker='.')
    plt.plot([i['date'] for i in Statistic()], [int(i['words_added']) for i in Statistic()], marker='.')
    plt.plot([i['date'] for i in Statistic()], [int(i['words_learned']) for i in Statistic()], marker='.')
    plt.plot([i['date'] for i in Statistic()], [int(i['words_deleted']) for i in Statistic()], marker='.')
    plt.plot([i['date'] for i in Statistic()], [int(i['load_times']) for i in Statistic()], marker='.')
    plt.plot([i['date'] for i in Statistic()], [int(i['fail']) for i in Statistic()], marker='.')
    plt.plot([i['date'] for i in Statistic()], [int(i['success']) for i in Statistic()], marker='.')
    plt.legend(['Time in learning(M)', 'Words added', 'Words learned', 'Words deleted', 'Load times', 'Fail count', 'Success count'])
    plt.show()
    