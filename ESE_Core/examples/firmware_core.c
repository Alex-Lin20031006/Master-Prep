/* Original teaching example: single-threaded only, no MMIO. */
#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#define CAP 8u
struct ring { uint8_t data[CAP]; size_t head, tail; };
static bool push(struct ring *r, uint8_t v) {
    size_t next = (r->head + 1u) % CAP;
    if (next == r->tail) return false;
    r->data[r->head] = v; r->head = next; return true;
}
static bool pop(struct ring *r, uint8_t *out) {
    if (r->head == r->tail) return false;
    *out = r->data[r->tail]; r->tail = (r->tail + 1u) % CAP;
    return true;
}
static bool decode_u16_le(const uint8_t *p, size_t n, uint16_t *out) {
    if (p == NULL || out == NULL || n < 2u) return false;
    *out = (uint16_t)((uint16_t)p[0] | ((uint16_t)p[1] << 8));
    return true;
}
static bool add_u32(uint32_t a, uint32_t b, uint32_t *out) {
    if (out == NULL || b > UINT32_MAX - a) return false;
    *out = a + b; return true;
}
int main(void) {
    struct ring r = {{0}, 0, 0}; uint8_t v = 0;
    uint16_t decoded = 0; uint32_t sum = 0;
    const uint8_t bytes[] = {0x34, 0x12};
    assert(decode_u16_le(bytes, 2, &decoded) && decoded == 4660);
    assert(!decode_u16_le(bytes, 1, &decoded));
    assert(!decode_u16_le(NULL, 2, &decoded));
    assert(add_u32(1, 2, &sum) && sum == 3);
    assert(!add_u32(UINT32_MAX, 1, &sum));
    assert(!pop(&r, &v));
    for (unsigned round = 0; round < 100; ++round) {
        for (unsigned i = 0; i < CAP - 1; ++i) assert(push(&r, (uint8_t)i));
        assert(!push(&r, 99));
        for (unsigned i = 0; i < CAP - 1; ++i) {
            assert(pop(&r, &v)); assert(v == i);
        }
        assert(!pop(&r, &v));
    }
    puts("PASS: decode, overflow guard, ring full/empty/wrap-around");
    return 0;
}
