import matplotlib.pyplot as plt

def epoch_ED_plot(log_ED, show=False, save=False, path='result_data/Train_hist.png'):
    x = range(len(log_ED['train_ED']))

    y1 = log_ED['train_ED']
    y2 = log_ED['val_ED']

    plt.plot(x, y1, label='train_ED')
    plt.plot(x, y2, label='val_ED')

    plt.xlabel('Epoch')
    plt.ylabel('ED')

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save:
        plt.savefig(path)

    if show:
        plt.show()
    else:
        plt.close()

def epoch_ED_plot_from_txt(path='result_data/Train_hist.png'):
    epoch_list = []
    train_ED_list = []
    test_ED_list = []
    train_PCK_list = []
    test_PCK_list = []

    with open(path, 'r') as rf:
        lines = rf.readlines()

    for line in lines:
        epoch_idx_from = line.find('[') + 1
        epoch_idx_to = line.find('/')
        train_ED_idx_from = line.find('mean of train ED: ') + 18
        train_ED_idx_to = line.find(' //')
        train_PCK_idx_from = line.find('train PCK: ') + 11
        train_PCK_idx_to = line.find(' ///')
        test_ED_idx_from = line.find('mean of test ED: ') + 17
        test_ED_idx_to = line.find(' ////')
        test_PCK_idx_from = line.find('test PCK: ') + 10
        test_PCK_idx_to = line.find('\n')

        if epoch_idx_from == 0:
            continue

        epoch = line[epoch_idx_from:epoch_idx_to]
        train_ED = line[train_ED_idx_from:train_ED_idx_to]
        test_ED = line[test_ED_idx_from:test_ED_idx_to]
        train_PCK = line[train_PCK_idx_from:train_PCK_idx_to]
        test_PCK = line[test_PCK_idx_from:test_PCK_idx_to]

        epoch_list.append(eval(epoch))
        train_ED_list.append(eval(train_ED))
        test_ED_list.append(eval(test_ED))
        train_PCK_list.append(eval(train_PCK))
        test_PCK_list.append(eval(test_PCK))

    plt.figure()
    plt.plot(epoch_list, train_ED_list, label='train_ED')
    plt.plot(epoch_list, test_ED_list, label='test_ED')
    plt.xlabel('epoch')
    plt.ylabel('ED')
    plt.tight_layout()
    plt.legend()
    plt.grid(False)
    plt.savefig('epoch_ED.png')
    plt.show()

    plt.figure()
    plt.plot(epoch_list, train_PCK_list, label='train_PCK')
    plt.plot(epoch_list, test_PCK_list, label='test_PCK')
    plt.xlabel('epoch')
    plt.ylabel('PCK')
    plt.tight_layout()
    plt.legend()
    plt.grid(False)
    plt.savefig('epoch_PCK.png')
    plt.show()

def frame_dist_plot_from_txt(path = 'result_data/inference_loss.txt') :
    frame_list = []
    ED_list = []
    PCK_list = []

    with open(path, 'r') as rf:
        lines = rf.readlines()

    for line in lines:
        frame_idx_from = line.find('[') + 1
        frame_idx_to = line.find(']')
        ED_idx_from = line.find('-') + 2
        ED_idx_to = line.find(' /')
        PCK_idx_from = line.find('/ ') + 2
        PCK_idx_to = line.find('\n')

        if frame_idx_from == 0:
            continue

        frame = line[frame_idx_from:frame_idx_to]
        ED = line[ED_idx_from:ED_idx_to]
        PCK = line[PCK_idx_from:PCK_idx_to]

        frame_list.append(eval(frame))
        ED_list.append(eval(ED))
        PCK_list.append(eval(PCK))

    plt.figure()
    plt.plot(frame_list, ED_list, label='ED')
    plt.xlabel('Frame')
    plt.ylabel('ED')
    plt.tight_layout()
    plt.legend()
    plt.grid(False)
    plt.savefig('Frame_ED.png')
    plt.show()

    plt.figure()
    plt.plot(frame_list, PCK_list, label='PCK')
    plt.xlabel('Frame')
    plt.ylabel('PCK')
    plt.tight_layout()
    plt.legend()
    plt.grid(False)
    plt.savefig('Frame_PCK.png')
    plt.show()


def draw_stickfigure3d(mocap_track, frame, data=None, joints=None, draw_names=False, ax=None, figsize=(8, 8)):
    #from mpl_toolkits.mplot3d import Axes3D

    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_aspect(1)

    if joints is None:
        joints_to_draw = mocap_track.skeleton.keys()
    else:
        joints_to_draw = joints

    if data is None:
        df = mocap_track.values
    else:
        df = data

    for joint in joints_to_draw:
        parent_x = df['%s_Xposition' % joint][frame]
        parent_y = df['%s_Zposition' % joint][frame]
        parent_z = df['%s_Yposition' % joint][frame]
        # ^ In mocaps, Y is the up-right axis

        ax.scatter(xs=parent_x,
                   ys=parent_y,
                   zs=parent_z,
                   alpha=0.6, c='b', marker='o')

        children_to_draw = [c for c in mocap_track.skeleton[joint]['children'] if c in joints_to_draw]

        for c in children_to_draw:
            child_x = df['%s_Xposition' % c][frame]
            child_y = df['%s_Zposition' % c][frame]
            child_z = df['%s_Yposition' % c][frame]
            # ^ In mocaps, Y is the up-right axis

            ax.plot([parent_x, child_x], [parent_y, child_y], [parent_z, child_z], 'k-', lw=2, c='black')

        if draw_names:
            ax.text(x=parent_x + 0.1,
                    y=parent_y + 0.1,
                    z=parent_z + 0.1,
                    s=joint,
                    color='rgba(0,0,0,0.9')

    return ax


# frame_dist_plot_from_txt(path = 'result_data/exp1/inference_loss.txt')
