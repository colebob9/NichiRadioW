import datetime
import pandas as pd
import pandas_read_xml as pdx
# import matplotlib
import matplotlib.pyplot as plt
import os


def make_graph(xmlFile):

    df = pdx.read_xml(
        xmlFile, ['packet', 'chat'], encoding='utf-8')

    # ------------------------------- Clean up xml -------------------------- #
    print(df)

    # drop unnecessary columns
    df.drop(['@thread', '@no', '@premium', '@anonymity', '@user_id', '@mail',
            '@leaf', '@score', '@deleted', '@date_usec', '@date'],
            axis=1, inplace=True)

    # drop rows without anything in the text column
    df.dropna(subset=['#text'], inplace=True)

    # rename columns
    df.rename(columns={"@vpos": "vpos", "#text": "text"}, inplace=True)

    # to numeric for accurate sorting
    df.vpos = df.vpos.astype(float)
    df.sort_index(inplace=True)

    # sort by vpos
    df.sort_values(by='vpos', kind="mergesort",
                   inplace=True, ignore_index=True)
    df['vpos'] = pd.to_numeric(df['vpos'], downcast='integer')    # back to int
    print(df)

    # --------------------- Loop through text columns for w's --------------- #
    w_list = ['ｗ', 'w', 'W']
    w_stats = dict.fromkeys(w_list, 0)
    w_amounts = []

    for index, row in df.iterrows():
        # print(row['vpos'], row['text'])
        w_total_amount = 0

        for w in w_list:
            w_count = row['text'].count(w)
            if w_count > 0:
                # print(f"Found {w} in DF index {index}. Counted {w_count} times.")
                # print(f"vpos: {row['vpos']}")
                # print(row['text'])
                # print('')
                w_stats[w] = w_stats[w] + w_count
                w_total_amount = w_count

        w_amounts.append(w_total_amount)

    print(w_stats)
    # print(w_amounts)

    print(len(w_amounts))

    # --------------------------- matplotlib graphing ----------------------- #
    # MPL setup
    plt.figure(figsize=(25, 15))
    plt.title("Number of W's in video")
    plt.xlabel("Video Pos")
    plt.ylabel("Number of W's")
    plt.legend()

    # make vpos into timestamps
    vpos_list = df['vpos'].values.tolist()
    print(len(vpos_list))
    # print(vpos_list)
    vpos_stamps = []

    for v in vpos_list:
        vpos_stamps.append(datetime.datetime.fromtimestamp(v/1000.0))

    x = vpos_list
    y = w_amounts
    plt.plot(x, y)
    # plt.bar(x, y, align='center')
    # plt.scatter(x,y)
    # for i in range(len(y)):
    #     plt.hlines(y[i], 0, x[i])  # Here you are drawing the horizontal lines

    plt.savefig(xmlFile + '.png', dpi=300, orientation='landscape')
    # plt.show()


for subdir, dirs, files in os.walk("NichiXML"):
    for file in files:
        make_graph("NichiXML/" + file)
