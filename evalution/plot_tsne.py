import matplotlib.pyplot as plt
from sklearn import manifold
import glob
import numpy as np
import matplotlib as mpl


speakers = ['p225', 'p226', 'p227', 'p228', 'p229', 'p230', 'p231', 'p232', 'p233', 'p234']
# proposed_speakers = ['p229', 'p231', 'p232']
proposed_speakers = []

# speakers = ['BDL (M, L1)', 'YKWK (M, KR)']
# # baseline_speakers = ['FAC-B (TXHC + L1)', 'FAC-B (YKWK + L1)']
# proposed_speakers = ['src_BDL_ref_TXHC (TXHC + L1(BDL))', 'src_CLB_ref_YKWK (YKWK + L1(CLB))']
# # proposed_speakers = ['src_BDL_ref_YKWK (voice YKWK)']


all_speakers = speakers + proposed_speakers
# markers = ["d", "d", "o", "o", "^", "^", "p", "p", "P", "P"]
# fac_markers = ["s", "v"]


all_embedings = []
speaker_labels = []
for sp in all_speakers:
    speaker = sp.split(" ")[0]
    speaker_file_list = sorted(glob.glob(f"../dataset/VCTK/dataset/spmel/{speaker}/*.npy"))
    print(f"Number of source utterances: {len(speaker_file_list)}.")
    # t = np.load(speaker_file_list[0])
    cnt = 0
    # print(speaker_file_list)
    # speaker_file_list = random.shuffle(speaker_file_list)
    for spf in speaker_file_list:
        if cnt > 40:
            break
        all_embedings.append(np.load(spf))
        speaker_labels.append(sp)
        cnt = cnt +1

print(np.array(all_embedings).shape)

print("Computing t-SNE embedding - speaker")
tsne_sp = manifold.TSNE(n_components=2, init='pca', random_state=0)
# tsne_sp = UMAP(n_components=2, init='spectral', random_state=0)
speaker_tsne = tsne_sp.fit_transform(np.array(all_embedings))
print(speaker_tsne.shape)
colors =  mpl.cm.get_cmap('tab20')(np.arange(12))
plt.figure(figsize=(12,8))
speakers_all = all_speakers
# markers_all = markers + fac_markers
# for speaker, c, m in zip(speakers_all, colors, markers_all):
for speaker, c in zip(speakers_all, colors):
    X_speaker_embedding = speaker_tsne[np.where(speaker==np.array(speaker_labels))]
    print(X_speaker_embedding.shape, speaker)
    plt.scatter(X_speaker_embedding[:,0], X_speaker_embedding[:,1], label=speaker, marker='x', color=c)
    plt.text(X_speaker_embedding[-1,0], X_speaker_embedding[-1,1], speaker)

plt.legend()
plt.tight_layout()
plt.savefig("embed_viz/tsne_10p5_itr.png", format='png')

# print("Computing t-SNE embedding - speaker")
# tsne_sp = manifold.TSNE(n_components=3, init='pca', random_state=0)
# speaker_tsne = tsne_sp.fit_transform(np.array(all_embedings))
# print(speaker_tsne.shape)
# colors =  mpl.cm.get_cmap('tab20')(np.arange(12))
# plt.figure(figsize=(12,8))
# fig = pylab.figure()
# ax = fig.add_subplot(111, projection = '3d')

# speakers_all = all_speakers
# markers_all = markers + fac_markers
# for speaker, c, m in zip(speakers_all, colors, markers_all):
#     X_speaker_embedding = speaker_tsne[np.where(speaker==np.array(speaker_labels))]
#     print(X_speaker_embedding.shape, speaker)
#     ax.scatter(X_speaker_embedding[:,0], X_speaker_embedding[:,1],X_speaker_embedding[:,2], label=speaker, marker=m, color=c)
#     # ax.text(X_speaker_embedding[-1,0], X_speaker_embedding[-1,1],X_speaker_embedding[-1,2], speaker)

# # plt.legend()
# plt.tight_layout()
# plt.savefig("embed_viz/SpeakerEmbeddings_ppg2ppg.png", format='png')