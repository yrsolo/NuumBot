import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from IPython.display import clear_output


def generate_test_data():
    """
    Generates test data for the activity log.
    """

    def random_like():
        return random.choice([True, False])

    test_log = [
        [
            {'name': 'test2', 'like': random_like(), 'sticker': random_like(), 'subscribe': random_like(), 'mode': 'rec',
             'time': pd.Timestamp.now() + pd.Timedelta(minutes=random.randint(-300, 300))},
            {'name': 'test2', 'like': random_like(), 'sticker': random_like(), 'subscribe': random_like(), 'mode': 'subs',
             'time': pd.Timestamp.now() + pd.Timedelta(minutes=random.randint(-300, 300))}
        ]
        for _ in range(300)
    ]
    return pd.DataFrame(sum(test_log, []))


def plot_activity_logs(log: pd.DataFrame, window_size: int = 5):
    """
    Plots activity logs for likes, subscriptions, and stickers.

    Parameters:
    log (pd.DataFrame): DataFrame containing the activity log with columns 'time', 'like', 'subscribe', and 'sticker'.
    window_size (int): Size of the rolling window in minutes (default is 5).
    """
    log = log.copy()
    log['minute'] = log['time'].dt.floor('min')  # Round to nearest minute

    def prepare_data(log, activity_column, window_size=window_size):
        actions_per_minute = log.groupby('minute')[activity_column].sum().reset_index(name='actions')
        # Calculate rolling sum
        actions_per_minute['rolling_sum'] = actions_per_minute['actions'].rolling(window=window_size, min_periods=1).sum()

        return actions_per_minute

    # Prepare data for each activity type
    like_data = prepare_data(log, 'like')
    subscribe_data = prepare_data(log, 'subscribe')
    sticker_data = prepare_data(log, 'sticker')

    # Plot each activity type
    plt.figure(figsize=(12, 6))
    for data, label, color in zip([like_data, subscribe_data, sticker_data],
                                  ['Likes', 'Subscriptions', 'Stickers'],
                                  ['blue', 'green', 'orange']):
        if len(data) > 0:
            plt.plot(data['minute'], data['rolling_sum'], label=f'{label}', lw=2, color=color)

    # Add limit line
    plt.axhline(y=5 * window_size, color='r', linestyle='--', label=f'5 actions / min)')

    # Format x-axis as hours and minutes
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xlabel('Time (Hours:Minutes)')
    plt.ylabel('Number of Actions')
    plt.title(f'Activity Logs Over Time (Rolling Window: {window_size} Minutes')
    plt.legend()
    plt.grid(True)
    plt.show()


def viz_log(log, i, N, c, current_mode='rec'):
    mode = {'rec': 'Рекоммендации', 'subs': 'Подписчики'}
    clear_output()
    for m, name in mode.items():
        df = log[log['mode'] == m]
        all = len(df)
        like = df['like'].astype(int).sum()
        sticker = df['sticker'].astype(int).sum()
        subs = df['subscribe'].astype(int).sum()
        if current_mode == m:
            print(name, f' цикл {c}: ({i}/{N})')
        else:
            print(name)
        print(f'Всего: {all}, лайкнул: {like}, стикер: {sticker}, подписался:{subs}')
        print(', '.join(df.tail(20)['name'].tolist()))
    plot_activity_logs(log, window_size=5)


if __name__ == '__main__':
    test_log = generate_test_data()
    viz_log(test_log, 2, 10, 4)
