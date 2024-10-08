import kue from 'kue'

const queue = kue.createQueue({name: 'push_notification_code'});

const jobdata = {
    phoneNumber: '07112547893',
    message: 'Hello, this is a test notification!',
};
const job = queue.create('push_notification_code', jobdata);

job
  .on('enqueue', () => {
    console.log('Notification job created:', job.id);
  })
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed attempt', () => {
    console.log('Notification job failed');
  });
job.save();