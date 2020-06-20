from matplotlib import pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle
import pandas as pd
import matplotlib as mpl
import seaborn as sns

cmap = plt.cm.YlOrRd_r
filename = "kobe_data.csv"
raw = pd.read_csv(filename)
kobe = raw[pd.notnull(raw['shot_made_flag'])]
kobe_nomade = kobe[kobe['shot_made_flag'] == 0]
kobe_made = kobe[kobe['shot_made_flag'] == 1]

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax



def colormap():
    """
    颜色转换
    """
    return mpl.colors.LinearSegmentedColormap.from_list('cmap', ['#C5C5C5', '#9F9F9F', '#706A7C', '#675678',
                                                                 '#713A71','#9D3E5E', '#BC5245',  '#C86138',
                                                                 '#C96239', '#D37636', '#D67F39', '#DA8C3E',
                                                                 '#E1A352'], 256)



def shot_make():

    axs = draw_court(lw=2)

    # 设置坐标轴范围
    axs.set_xlim(-250, 250)
    axs.set_ylim(422.5, -47.5)
    # 消除坐标轴刻度
    axs.set_xticks([])
    axs.set_yticks([])
    # 添加备注信息
    #plt.annotate('', xy=(100, 160), xytext=(178, 418))
    #plt.show()

    # 画图操作-投篮位置信息
    axs.scatter(kobe_nomade.loc_x, kobe_nomade.loc_y, s=15, marker='x', color='#A82B2B')
    axs.scatter(kobe_made.loc_x, kobe_made.loc_y, s=15, marker='o', edgecolors='#3A7711', color="#F0F0F0", linewidths=2)
    plt.show()

def joint_shot_chart():
    joint_shot_chart = sns.jointplot(kobe.loc_x, kobe.loc_y, stat_func=None,
                                     kind='scatter', space=0, alpha=0.5)
    ax = joint_shot_chart.ax_joint
    # 添加篮球场
    ax = draw_court(ax=ax)
    ax.set_xlim(-250, 250)
    ax.set_ylim(422.5, -47.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(labelbottom='off', labelleft='off')
    plt.show()


def shot_heatmap():
    # 绘制球员投篮热力图
    shot_heatmap = sns.jointplot(kobe.loc_x, kobe.loc_y,
                                 stat_func=None, kind='kde', space=0, color=cmap(0.1),
                                 cmap=colormap(), n_levels=100)
    # 设置图像大小
    shot_heatmap.fig.set_size_inches(12, 11)
    # 图像反向
    ax = shot_heatmap.ax_joint
    # 添加篮球场
    ax = draw_court(ax=ax, color='w', lw=2)
    ax.set_xlim(-250, 250)
    ax.set_ylim(422.5, -47.5)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(labelbottom='off', labelleft='off')

    # 将坐标轴颜色更改为白色
    lines = plt.gca()
    lines.spines['top'].set_color('none')
    lines.spines['left'].set_color('none')
    # 去除坐标轴标签
    ax.axis('off')

    # draw color bar
    fig = plt.figure(figsize=(12, 8))
    ax2 = fig.add_axes([0.92, 0.1, 0.02, 0.8])
    cb = mpl.colorbar.ColorbarBase(ax2, cmap=colormap(), orientation='vertical')
    cb.set_label('FGA(Field goal attempts)')
    cb.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])
    cb.set_ticklabels(['0', '10', '20', '30', '40'])
    plt.show()