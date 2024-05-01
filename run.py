from preprocess import preprocess
from train import train
from testing import testing

print('Execution start')
preprocess()
print('Finished preprocess')
train()
print('Finished training')
testing()
print('Finished testing')

