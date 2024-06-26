/*
 * This file is part of the Micro Python project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2021 Dan Halbert for Adafruit Industries
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#ifndef MICROPY_INCLUDED_SHARED_MODULE_KEYPAD_EVENTQUEUE_H
#define MICROPY_INCLUDED_SHARED_MODULE_KEYPAD_EVENTQUEUE_H

#include "py/obj.h"
#include "py/ringbuf.h"

typedef struct _keypad_eventqueue_obj_t keypad_eventqueue_obj_t;

struct _keypad_eventqueue_obj_t {
    mp_obj_base_t base;
    ringbuf_t encoded_events;
    bool overflowed;
    void (*event_handler)(keypad_eventqueue_obj_t *);
};

bool keypad_eventqueue_record(keypad_eventqueue_obj_t *self, mp_uint_t key_number, bool pressed, mp_obj_t timestamp);

#endif  // MICROPY_INCLUDED_SHARED_MODULE_KEYPAD_EVENTQUEUE_H
