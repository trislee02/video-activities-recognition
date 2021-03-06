setwd('C:/Users/Admin/Desktop')

df = read.csv("ucf101_analyze_3.csv")
#df = read.csv("result_on_train_set.csv")
attach(df)
names(df)

corrects = frame_id[true_label == top_1_label]
acc = length(corrects) / length(frame_id); acc

corrects = frame_id[true_label == top_1_label | true_label == top_2_label]
top2acc = length(corrects) / length(frame_id); top2acc

corrects = frame_id[true_label == top_1_label | true_label == top_2_label | true_label == top_3_label]
top3acc = length(corrects) / length(frame_id); top3acc

hist(top_1_score)

### Top 1 score - top 2 score
delta12 = top_1_score - top_2_score
h = hist(delta12, plot=FALSE)
h$density = h$counts/sum(h$counts)*100
plot(h, freq=FALSE)

### Phan tram top1 - top2 thoa dieu kien
x = seq(0.05, 1, by=0.05)
pArr = c()
pSet = c()
for (DELTA in x)
{
  delta12 = top_1_score - top_2_score
  conditions = delta12 < DELTA
  pDelta12 = length(delta12[conditions]) / length(delta12)
  ### Phan tram top1 d?ng
  pWrongPred = length(top_1_label[(top_1_label != true_label) & (conditions)]) / length(top_1_label)
  ### p(pred = false | top1 - top2 < DELTA)
  p = pWrongPred / pDelta12; 
  pArr = append(pArr, p)
  pSet = append(pSet, pWrongPred)
}
pArr
par(mfrow=c(1,2))
plot(x,pArr, main='p(pred = wrong|top1 - top2 < delta)', xlab='delta', ylab='p')
plot(x,pSet, main='p(pred = wrong, top1 - top2 < delta)', xlab='delta', ylab='p')

### Phan tram top1 thoa dieu kien
x = seq(0.05, 1, by=0.05)
pArr = c()
pSet = c()
for (DELTA in x)
{
  conditions = top_1_score <= DELTA
  pCondition = length(top_1_score[conditions]) / length(top_1_score)
  ### Phan tram top1 d?ng
  pWrongPred = length(top_1_label[(top_1_label != true_label) & (conditions)]) / length(top_1_label)
  ### p(pred = false | top1 - top2 < DELTA)
  p = pWrongPred / pCondition; 
  pArr = append(pArr, p)
  pSet = append(pSet, pWrongPred)
}
pArr
par(mfrow=c(1,2))
plot(x,pArr, main='p(pred = wrong|top1 < delta)', xlab='delta', ylab='p')
plot(x,pSet, main='p(pred = wrong, top1 < delta)', xlab='delta', ylab='p')

library(dplyr)
df_grp_vid = df %>% group_by(video_id, true_label, top_1_label) %>%
  summarise(total_vote = mean(top_1_score),
            .groups = 'drop')
View(df_grp_vid)