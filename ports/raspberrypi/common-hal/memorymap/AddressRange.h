/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2020 microDev
 * Copyright (c) 2023 Bob Abeles
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

#ifndef MICROPY_INCLUDED_RASPBERRYPI_COMMON_HAL_MEMORYMAP_ADDRESSRANGE_H
#define MICROPY_INCLUDED_RASPBERRYPI_COMMON_HAL_MEMORYMAP_ADDRESSRANGE_H

#include "py/obj.h"

// depending on the section memory type, different access methods and rules apply
typedef enum { SRAM, ROM, XIP, IO } memorymap_rp2_section_t;

typedef struct {
    mp_obj_base_t base;
    uint8_t *start_address;
    size_t len;
    memorymap_rp2_section_t type;
} memorymap_addressrange_obj_t;

typedef struct {
    uint8_t *start_address;
    size_t len;
    memorymap_rp2_section_t type;
} addressmap_rp2_range_t;

#endif // MICROPY_INCLUDED_RASPBERRYPI_COMMON_HAL_MEMORYMAP_ADDRESSRANGE_H
