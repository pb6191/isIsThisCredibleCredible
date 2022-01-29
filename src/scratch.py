import numpy as np

scores = np.random.randn(10)
likelihood = np.random.randn(10)

dt = pd.DataFrame({"scores": scores, "likelihood": likelihood})

dt.corr()
import seaborn as sns

sns.pairplot(dt)


#%% plot results

fig, ax = plt.subplots(1, 2, figsize=(13, 5))

ax[0].plot(train_acc, "ro-")
ax[0].plot(test_acc, "bs-")
ax[0].set_label("Epochs")
ax[0].set_label("Accuracy (%)")
ax[0].legend(["Train", "Test"])

ax[1].plot(losses)
ax[1].set_xlabel("Epochs")
ax[1].set_ylabel("Loss")
plt.show()
