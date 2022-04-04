#ifndef ASCII_TRACE_DEFINITION_H
#define ASCII_TRACE_DEFINITION_H

enum class Trace_Time_Unit { PICOSECOND, NANOSECOND, MICROSECOND};//The unit of arrival times in the input file
#define PicoSecondCoeff  1000000000000	//the coefficient to convert picoseconds to second
#define NanoSecondCoeff  1000000000	//the coefficient to convert nanoseconds to second
#define MicroSecondCoeff  1000000	//the coefficient to convert microseconds to second
#define ASCIITraceTimeColumn 0
#define ASCIITraceDeviceColumn 1
#define ASCIITraceAddressColumn 2
#define ASCIITraceSizeColumn 3
#define ASCIITraceTypeColumn 4
#define ASCIITraceWriteCode "0"
#define ASCIITraceReadCode "1"
#define ASCIITraceBufferReadCode "2"
#define ASCIITraceBufferWriteCode "3"
#define ASCIITraceComputeCode "4"
#define ASCIITraceUpperTransferCode "5"
#define ASCIITraceLowerTransferCode "6"
#define ASCIITraceWriteCodeInteger 0
#define ASCIITraceReadCodeInteger 1
#define ASCIITraceBufferReadCodeInteger 2
#define ASCIITraceBufferWriteCodeInterger 3
#define ASCIITraceComputeCodeInterger 4
#define ASCIITraceUpperTransferCodeInteger 5
#define ASCIITraceLowerTransferCodeInterger 6
#define ASCIILineDelimiter ' '
#define ASCIIItemsPerLine 5

#endif // !ASCII_TRACE_DEFINITION_H
