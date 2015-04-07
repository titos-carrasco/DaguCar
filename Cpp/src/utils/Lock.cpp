#include "Lock.h"

Lock::Lock()
{
    if( pthread_mutex_init( &_lock, NULL ) != 0 )
    {
        throw -1;
    }
}

Lock::~Lock()
{
    pthread_mutex_destroy( &_lock );
}

void Lock::lock()
{
    pthread_mutex_lock( &_lock );
}

void Lock::unlock() {
    pthread_mutex_unlock( &_lock );
}
