import matplotlib.pyplot as plt

from energize import third_floor_temperatures as tft


def main():
    df = tft.get_temperatures()
    hist = df.hist(bins=10, column="presentValue")
    plt.show()


if __name__=="__main__":
    main()

