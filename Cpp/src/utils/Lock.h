#ifndef LOCK_H
#define LOCK_H

#include <pthread.h>

class Lock
{
    private:
        pthread_mutex_t _lock;

    public:
        Lock();
        ~Lock();
        void lock();
        void unlock();
};

#endif // LOCK_H
